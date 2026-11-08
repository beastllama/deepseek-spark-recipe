# November 7–8, 2026 observations

## Historical v0.1 speed measurements

The speed jobs below used image `sha256:dac7945c079d491bb1f757f2a9b376abd55f80e59835d303333eac192cb85a25` and source closure `4df32ee4…`. They were not rerun on v0.2. [Historical build identity](data/build-identity-v0.1.json).

These results describe one selected deployment on **two DGX Sparks**, with Mia EAQ v1 + matching Keys, TP=2, 524,288 shared context, eight admitted lanes, 32 internal streams and a 1 GiB prompt cache. Both jobs ran through SparkDash, approximately 19:54–19:57 America/Chicago. [Machine-readable data](data/results.json).

| Observation | Result |
| --- | ---: |
| Cold 128K calibrated TTFT-derived prefill | 2,232.53 tok/s |
| Actual prompt tokens per measured prefill sample | 131,094 |
| Prefix-cache reuse in both measured prefill samples | 0 |
| Eight-user aggregate decode | 311.10 tok/s |
| Mean individual decode | 42.55 tok/s |
| Mean first reasoning/content token | 924.45 ms |
| Mean first answer token | 2,425.92 ms |
| Measured decode requests completed | 8/8 |

The 128K UI collector used two measured samples after two warmups and three small overhead calibrations. It selected the lower-rate successful sample. That sample's raw TTFT was 58,898.28 ms and calibrated overhead 178.34 ms. Both measured prompts explicitly reported cached=0. No model restart, model-cache flush or OS-cache flush was used; cold means no reusable prompt prefix, with the model already resident.

The decode job used Structured counting, Empty added context, exactly eight concurrent requests, temperature 0, top-k 20, thinking on and 400 output tokens per request. Each measured request had 58 prompt tokens, cached=0 and 400 completion tokens, ending at `finish_reason=length`. The wave lasted 10,466.45 ms. Aggregate rate counts 3,192 post-first-token outputs over the earliest-first to latest-last token interval. It is not the mean individual rate multiplied by eight. Individual rates were 39.79–45.41 tok/s, median 42.19 tok/s.

The first token can be reasoning; the first answer token is a separate measurement. All eight first-token offsets were 204.27–1,642.38 ms, preceding the earliest last-token offset of 10,228.14 ms. This supports overlapping eight-stream decode. It does not establish completed-answer quality: all streams hit the output cap.

The seven native prefill completions and nine decode completions, including built-in preparation, accounted for exactly 267,504 prompt tokens, matching the model counter increase. No foreign completion was observed in that interval. Both ranks retained their identities; restart/OOM, graph-fallback and preemption observations stayed zero. The benchmark changed no persistent model settings.

The supplied community comparison chart used four Sparks, different weights and methods, and claimed a median-of-three protocol. It is not a matched control. These two-Spark numbers do not establish engine rankings, device scaling, deep-context decode speed, or the isolated benefit of either new repair. A previous 228.54 tok/s cached 32-request wave is a separate experiment and should not be used to calculate a patch speedup from this 311.10 figure.

The two repaired bugs have controlled CPU counterexamples: rejected admission evicting reusable snapshots, and a global ContextFull backoff blocking later fitting work. Their narrow regression tests and existing controls support those causal fixes. The separate cold/warm 32K recall checks scored 16/16 each with no stale values and the same output fingerprint. Neither substitutes for a broad semantic-quality evaluation.

Saved job identifiers: prefill `54a3b8af-70a4-4543-bd5d-2d4fd75da278`; decode `cabfeab5-3401-4456-bcfa-8185f13a3969`.

## Matched long-history pressure check

Root cause: saved DeepSeek snapshots depended on compressed prefix rows in the reusable working KV pool. Evidence: the saved CPU overwrite counterexample returned overwritten packed bytes, and the matched pressure baseline reused only one of three long prefixes. v0.2 copies each complete packed prefix into independent backing on both ranks, charges its full size to the unchanged 1 GiB snapshot budget, and restores it after physical-row overwrite. Budget eviction still applies.

The baseline already contained the refused-cut-in guard (image `413dfa4f…`, closure `c3d01df8…`). The candidate was image `sha256:efceb406655ba9e7334e77f6ed0ff4511ac1d0ec7c471f2d66a70e766aedc0ba`, closure `e6581809…`. This is a separate comparison from the historical short-prompt jobs. [Sanitized numeric export](data/pressure-results.json).

| Observation | Cut-in baseline | Full-prefix backing |
| --- | ---: | ---: |
| Measured three-stream wave | 168.110 s | 6.747 s |
| Whole cold benchmark job | 404.468 s | 242.435 s |
| Initial cold priming | 235.730 s | 235.050 s |
| Mean first streamed token | 83.041 s | 0.999 s |
| Fully reused long prefixes | 1/3 | 3/3 |
| Native reused / prompt tokens | 169,856 / 510,123 | 509,568 / 510,126 |

The measured wave took **95.99% less time**; including cold priming, the entire benchmark job took **40.06% less time**. Cold prefill was essentially unchanged. These are elapsed-time reductions in one cache-pressure scenario, not isolated decode-kernel or whole-project speedups.

Both arms used SparkDash Structured counting, concurrency 3, target context 170,000, output cap 400, temperature 0.7, top-k 20 and thinking on. Weights, matching Keys, precision, High effort, 524,288-token shared pool, eight admitted slots and snapshot budget stayed the same. The salted actual prompts were 170,041 tokens before and 170,042 after. All three measured streams in each arm completed 400 tokens. The candidate reused 169,856 tokens in each measured stream; its last cache report charged 489/1,024 MiB with four states and zero reported budget evictions, refusals or failures.

Method: capture a cold 32K recall check; run the matched long-context jobs through SparkDash, including each arm's cold primers and measured follow-up wave; then repeat the warm 32K recall after pressure has overwritten working rows. Cold and post-overwrite recall each scored **16/16**, with zero stale values, 116 output tokens and the same output fingerprint. The warm check reused 36,736 of 36,910 prompt tokens. This checks the 32K recall scenario; it does not establish 170K retrieval accuracy or broad semantic quality.

This is **one paired sample**, with different salts and stochastic output. Both job intervals included the 32-token warmup; the baseline also contained two unrelated tiny completions. Equal native completion tuples corroborate the UI totals without identifying individual requests. Full output-reservation behavior and whole-project finish time remain unmeasured.

## Passive real work after repair

Two saved samples at 05:56:38 and 05:57:27 UTC on November 8 covered all-client model completions after repair verification on the same full-prefix runtime. **41 completed model calls reused 4,581,248 of 4,959,770 prompt tokens (92.37%)**; median prompt length was 147,908 tokens. The ten calls added between samples reused **1,521,664 of 1,539,096 tokens (98.87%)**. [Sanitized numeric export](data/live-work-results.json).

The queue showed zero waiting at both samples, with two then one running request. Both ranks had zero OOM/restarts and no reported throttling. Retained backing rose from 954 to 957/1,024 MiB and cumulative budget evictions from 22 to 25; those budget evictions are distinct from physical-prefix invalidation. No large-prefix physical invalidation or relocation failure was reported in the bounded logs. One client-left event had unknown cause.

These are all-client model steps, not completed projects or a controlled latency comparison. Two samples can miss brief waits; one or two running requests do not demonstrate eight-lane saturation. The observation does not measure answer quality or whole-project completion gain. No new live reads, generation, benchmark or model action was performed for this publication update.
