# Shared KV pool admission benchmark

On a two-DGX-Spark DeepSeek V4.1 Flash setup, raising the shared KV pool from 524,288 to 655,360 positions let four roughly 115K-token requests run concurrently instead of three. Both arms kept a 524,288-token limit per request, a full 32,768-token output allowance, High reasoning, eight API slots, and the same pinned EAQ v1 weights and matching Keys. This measures a batch of completed requests and the wait before an answer starts.

## Reproduce the engine pair

Use two DGX Sparks with the [pinned model, Keys, Engram and kernel kit](README.md#external-assets). Build and configure the two arms on the same hardware and retain both ranks’ normal memory and thermal protection. Use the recipe’s [native build and launch instructions](README.md#build). Stop the running pair using your normal controls and verify both ranks have stopped before switching builds. Each arm needs matching binaries on both ranks.

Start with the [v0.3.0 source reconstruction](README.md#exact-source) and its four patches in order. From this recipe’s root, with that verified checkout at `tensorfold/`:

```sh
git -C tensorfold apply --check ../patches/admission-baseline.patch
git -C tensorfold apply ../patches/admission-baseline.patch
python3 scripts/verify-source.py tensorfold --manifest data/source-manifest-admission-baseline.json
```

Build this tree and run it with `ADMISSION_PROFILE=baseline` in both ranks’ `runtime.env`. Then apply the capacity patch, verify the new closure, and build again using the same toolchain and assets:

```sh
git -C tensorfold apply --check ../patches/shared-pool-capacity.patch
git -C tensorfold apply ../patches/shared-pool-capacity.patch
python3 scripts/verify-source.py tensorfold --manifest data/source-manifest-admission-shared-pool.json
```

Use `ADMISSION_PROFILE=shared-pool` in both ranks’ `runtime.env` for that build. The included [launch adapter](scripts/launch-rank.sh) sets the larger pool on both ranks and retains the 524,288-token request window. Both benchmark profiles set the same cached-fill piece limit of 16,384 on the head and use 64-row rounds, 32 internal streams, and a 1 GiB prompt snapshot store. The store budget and the KV pool are independent. `admission-baseline.patch` restores the cumulative changes since v0.3.0. The second patch is the only engine delta between the two arms. It adds about 111.25 MiB of compressed cache planes per rank before allocator rounding. GPU kernel sources and the 21 retained build fatbins are identical across the recorded pair.

The source manifests verify 1,117 files for the baseline and 1,118 for the larger pool. Published image digests identify the measured local artifacts. A clean public hardware build and independent reproduction are pending.

## Reproduce the SparkDash workload

On Linux, use a separate checkout and configuration for the benchmark dashboard. With the recipe in the current directory, use Node 22.19 or newer in the 22.x series and SparkDash’s lockfile:

```sh
git clone https://github.com/MiaAI-Lab/sparkDash.git sparkdash-admission
git -C sparkdash-admission checkout --detach 24daeb57390a33b414cec214200625b0a3dcb736
git -C sparkdash-admission apply --check ../patches/sparkdash-2.90-admission-benchmark.patch
git -C sparkdash-admission apply ../patches/sparkdash-2.90-admission-benchmark.patch
cd sparkdash-admission
npm ci
npm run typecheck
npm run build
BIND_HOST=127.0.0.1 npm start
```

The [SparkDash patch](patches/sparkdash-2.90-admission-benchmark.patch) includes the synthetic workload and the streaming, counter and capacity collectors it uses. It targets the pinned 2.90.0 source. For the isolated fixture, configure a monitored local TensorFold target with the normal SparkDash setup. The collector checks the Linux listener and its actual `--context` argument. It needs ordinary read access to that process, its model metadata and its healthy endpoint. For the larger-pool arm, `/health` must also report the expected `pool_tokens`. Keep both services on an authenticated or private path and leave the fixture’s idle and capacity checks enabled. On a host already running SparkDash, choose an unused dashboard port with `PORT`.

1. Confirm that both ranks are ready and the engine has zero running and waiting requests. In **SparkDash → Decode**, choose the monitored TensorFold port, Structured, and **Cached-tail measurement → Admission · four requests, 32K allowance, natural completion**. Turn off other synthetic samplers and keep unrelated traffic out of the measurement.
2. The dashboard generates a fresh seeded synthetic reference, primes it once from cold cache with an eight-token output limit, and sends four continuations together with target tails of 1,024, 2,048, 4,096 and 8,192 tokens. The continuations request a short database backup checklist and run at temperature 0.7, top-p 1, top-k 20 and High reasoning. Each may generate up to 32,768 tokens and ends at its natural stop. The seed recorded for each run reproduces the synthetic filler. Use a fresh run in each arm so the primer starts cold.
3. Keep only samples with a zero-cache primer, four natural completions, and reported prompt/cache counts that pass the scenario’s validation. The guard polls every 250 ms and discards a sample if it sees outside work, a disconnect, or a reset or mismatch in native request counts. Confirm the final native completion delta is five including the primer. Record the full job separately from the four-request wave. Save first-content time, each request’s completion time and output length, and longest SSE pauses. Report the observed peak running and waiting counts. First-content time includes queuing, prefill and reasoning.
4. Repeat once with the same serving settings and the other arm. For a narrow correctness check, run SparkDash **Quality → Long-context recall**, 32K, two items. The recorded candidate scored 32/32 keys with no stale values or errors. Test more real workflows before drawing broader quality or throughput conclusions.

The generic history header in the tested dashboard can label this custom scenario temperature 0. Use the scenario’s saved request configuration and its 0.7 setting for comparison.

## Recorded results, November 15 Central time

| Metric | 524,288 pool | 655,360 pool |
| --- | ---: | ---: |
| Peak observed running requests | 3 | 4 |
| Full four-request wave | 42.445 s | 33.532 s |
| Full dashboard job including cold prime | 95.840 s | 87.069 s |
| Completions per minute during wave | 5.654 | 7.157 |
| Mean request completion | 30.286 s | 29.867 s |
| Mean first content | 24.086 s | 23.528 s |
| P95 of per-request longest SSE pause | 1.071 s | 1.530 s |
| Output tokens across four completed requests | 2,963 | 2,636 |

The allocator reserves `align_up(prompt_tokens + max_output_tokens + round_rows + 2, 2048)` positions. All four full reservations totaled 612,352 positions in both arms. Each completed request reused roughly 114.6K input tokens. The larger pool let the fourth reservation fit and the observed wave finished 21.0% sooner. Mean individual completion improved by 1.4%, and the P95 longest SSE pause grew by 0.458 s. Output lengths and prompt seeds differed, so the 26.6% increase in completions per minute is evidence from this one matched synthetic pair. The calculation excludes the cold primer. At other prompt sizes, eight long requests can still fill the shared pool.

The candidate’s measured interval had no observed OOM, restart or disconnect. Post-run available memory on the two Sparks was 7.31 GiB and 9.09 GiB, measured at one point. New deployments can have different headroom. The pauses measure gaps between SSE events, and 250 ms sampling can miss short scheduler transitions.

[Sanitized request and timing data](data/shared-pool-admission-results.json) · [Credits](CREDITS.md) · [Reproduction status](REPRODUCTION-STATUS.md)
