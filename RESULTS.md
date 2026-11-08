# November 7, 2026 observations

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
