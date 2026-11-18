# Short requests at a prefill yield on two DGX Sparks

A 61-token cold request with room for its entire output allowance waited **10.52 seconds** in the baseline queue. Three times, the scheduler admitted a longer request while the short one fit. One decoder was already running at the second decision. The short request needed 34,816 contiguous KV positions and 448,512 were available. It waited another 8.38 seconds.

The patch lets one later, same-priority cold text request of at most 2,048 tokens go first at an existing prefill yield. The backend checks the full aligned reservation against live streams and protected cache state. The attempt uses the parent prefill’s single allowance even if placement subsequently fails. The scheduler then gives decoding its next turn. Pending cancellations, a borrowed cache entry, a parked fill or an unavailable fit result prevent the overtake.

## What changed in SparkDash

One guarded five-job wave per arm used the same weights, matching Keys, High reasoning, 524,288 context, 32,768 output allowance, 786,432 shared KV positions, 1 GiB snapshot store and eight public lanes. All five replies in each arm reached a natural stop. The fresh cold primer is outside the wave times. [Per-request measurements](data/bounded-short-admission.json)

| Metric | Baseline | Short-request patch |
|---|---:|---:|
| Short request in queue | 10.52 s | 1.96 s |
| Short request, first streamed token | 10.73 s | 2.20 s |
| Short request, first visible answer | 31.43 s | 28.85 s |
| Short request, finished | 35.93 s | 33.31 s |
| Short request, longest stream gap | 0.45 s | 1.14 s |
| Time to finish all five jobs | 41.32 s | 34.81 s |
| Total generated tokens | 3,853 | 3,200 |
| Generated tokens per second of wave time | 93.26 | 91.93 |
| P95 longest stream gap across requests | 1.38 s | 1.14 s |

The short prompt and its **647 output tokens matched by hash**. Native telemetry recorded one overtake. The short request passed the 4K-tail request, which was admitted 307 ms later. All four long prompts still reused exactly 133,120 tokens each. The short request’s longest stream gap grew by 0.69 s, and the 4K-tail request finished 0.83 s later.

The long prompts used fresh seeds, the first two warm requests arrived in a different order and total output fell 16.95%. The 15.75% shorter wave is an observed outcome for this pair. Attributing the wave-time difference to the scheduler would require matched output work. Tool use, refusal rate and answer quality were outside this comparison.

## Reproduce the change

1. Follow [the existing 786,432 recipe](KV-POOL-786432.md), including its optional **numeric admission observation patch**. Use the same model assets and the prepared SparkDash five-request fixture. In the Linux checkout, verify the starting source, apply the scheduler overlay and verify the resulting source.

   ```sh
   python3 scripts/verify-source.py tensorfold --manifest data/source-manifest-kv-pool-admission-observation.json
   git -C tensorfold apply --check ../patches/bounded-short-admission.patch
   git -C tensorfold apply ../patches/bounded-short-admission.patch
   python3 scripts/verify-source.py tensorfold --manifest data/source-manifest-bounded-short.json
   ```

2. Build using the [native build instructions](README.md#build). The tested deployment replaced the head executable and retained the compatible follower and all 21 GPU fatbins. Use `ADMISSION_PROFILE=shared-pool-768` on both ranks. In the head’s runtime file, set `TF_AI_OPS_ADMISSION=1`, `TF_AI_OPS_YIELD=1` and `TF_AI_OPS_SPANS=1` for measurement. The scheduler opt-in is `TF_BOUNDED_SHORT_OVERTAKE=1` on the **head only**. The flag defaults off. The recorded baseline used the corrected observer executable and the candidate used the patched executable. Their hashes are in the measurements file.
3. At idle, run **SparkDash → Decode → Cached-tail measurement → KV pool comparison · five requests, 32K allowance** once per arm. Keep the same profile and guard against outside requests. Verify six completions including the prime, four equivalent cache hits, the full output allowances, and no new disconnects. Compare the `short_overtake` span’s request IDs against the actual native dequeues. Use the first streamed token, first visible answer and completion columns separately.

We verified that the published patch applies to the 1,119-file prerequisite and that all 1,120 resulting source files match the tested manifest. The measured ARM64 head passed its loader check on Spark. Independent hardware reproduction remains open.

The experiment builds on DeepSeek, Mia’s AI Lab, drowzeys’ Keys, Ash Hart and the TensorFold contributors, BertholomusAI’s native Spark work, and SparkDash’s benchmark and streaming collectors. The inherited tool, cache and kernel work is credited in the [full acknowledgments](CREDITS.md).
