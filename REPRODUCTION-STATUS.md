# Reproduction status

This publication contains measured results and an exact source/configuration recipe. **No new clean build, model start, asset download/preparation or generation run was performed to validate the public packaging.**

| Item | Evidence / status |
| --- | --- |
| Historical speed results | Saved v0.1 SparkDash jobs, 8/8 capped streams and two successful cold-prefix prefill samples; original image `dac7945c…`, not rerun on v0.2 |
| Long-history evidence | Separate paired 3×170K pressure sample and cold/post-overwrite 32K recall, plus passive all-client reuse observations; no whole-project gain measured |
| Tested source | 1,117-file v0.2 closure `e6581809b03c00c99f79f090ee4891dda0f3ee1b7bbb0159b78f8d2454a80b8c`; historical `4df32ee4…` manifest remains available |
| Public reconstruction | `fbbc97132cd004237d9887b8d3185896efaedc5c` plus all three patches in `data/patch-series.json` order; every recorded source file can be checked by `scripts/verify-source.py` |
| Source build | Saved local v0.2 native rebuild passed with retained GPU bundles and changed head/follower binaries; clean public ARM64/GPU build remains unexecuted |
| GPU bundles | 21 retained fatbin SHA-256 values published; exact CUDA source/build helper matches the public base pin; fresh toolchain byte equivalence remains unverified |
| Kernel kit | Public base-kit pin, exact 48-cubin release references, staging helper and expected merged AOT digest published; no binary assets redistributed |
| Model assets | Exact EAQ, Keys and Engram references plus narrow license metadata checks; operators acquire and prepare their own assets |
| Native launch | Actual selected argv/environment transcribed into a configurable single-rank adapter; new public adapter has not been used to start a pair |
| Source modifications | Earlier retained changes, refused-cut-in guard and full-prefix backing are included in the ordered series; the two earlier focused PRs alone are insufficient |
| Peer compatibility | v0.2 changes snapshot save/restore frames: head and follower must use the same updated build; no head-only replacement |
| Focused upstream port | The new full-prefix peer-specific port needs independent review/qualification; the earlier admission PRs do not contain it |
| Clean independent reproduction | Pending |

Remaining proof requirements before claiming a tested turnkey installer or byte-identical build:

1. Build the public packaging in a clean ARM64 environment and record the resolved NVIDIA base digest, compiler/nvcc versions, all fatbin hashes and both executable hashes. Compare them to the published retained artifacts. A different digest must be reported; do not relabel it as the measured image.
2. Prepare the pinned external assets through the authors' documented flows, including matching Keys and stock F16 draft tensors, rank-cache format, RoPE/token map and local Engram. The public recipe describes that acquisition path; it does not certify a newly prepared asset tree.
3. Verify both rank launches, readiness, supported memory/thermal guards, normal Start/Stop and recovery under the operator's own container integration. This repository intentionally contains no machine-specific controller.
4. Bind the exact SparkDash collector source/version and local overlay to a public pin. The published method/settings and saved results are known, but the complete dashboard overlay is not part of this engine source closure.
5. For any independent reproduction, save complete configurations, cached-token evidence and boundary counters for the stated UI protocol. Report cold priming, measured follow-up wave and whole benchmark job separately for pressure comparisons. Keep capped speed observations, narrow recall and passive reuse separate from completed-answer quality and whole-project finish time.

Publication static checks and source-patch verification should be recorded separately from model/runtime validation. Neither screenshots nor source review is a new runtime pass.
