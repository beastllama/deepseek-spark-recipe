# Reproduction status

This publication contains measured results and an exact source/configuration recipe. **No new clean build, model start, asset download/preparation or generation run was performed to validate the public packaging.**

| Item | Evidence / status |
| --- | --- |
| Measured result | Saved SparkDash jobs, native numeric completion metadata and sanitized data; 8/8 capped streams and two successful cold-prefix prefill samples |
| Tested source | Source-only export independently verified at 1,117 files, 9,872,803 bytes, closure `4df32ee4fc221d4e773542005750fd4fa411deed331ab2d8218fab5785eb85ce` |
| Public reconstruction | `fbbc97132cd004237d9887b8d3185896efaedc5c` plus `patches/tested-stack.patch`; every recorded source file can be checked by `scripts/verify-source.py` |
| Source build | Public pinned upstream build procedure, Zig archive hash and source-controlled per-kernel flags documented; no fresh publication build executed |
| GPU bundles | 21 retained fatbin SHA-256 values published; exact CUDA source/build helper matches the public base pin; fresh toolchain byte equivalence remains unverified |
| Kernel kit | Public base-kit pin, exact 48-cubin release references, staging helper and expected merged AOT digest published; no binary assets redistributed |
| Model assets | Exact EAQ, Keys and Engram references plus narrow license metadata checks; operators acquire and prepare their own assets |
| Native launch | Actual selected argv/environment transcribed into a configurable single-rank adapter; new public adapter has not been used to start a pair |
| Source modifications | Earlier retained changes are included in the complete overlay; the two focused PRs alone are insufficient |
| Clean independent reproduction | Pending |

Remaining proof requirements before claiming a tested turnkey installer or byte-identical build:

1. Build the public packaging in a clean ARM64 environment and record the resolved NVIDIA base digest, compiler/nvcc versions, all fatbin hashes and both executable hashes. Compare them to the published retained artifacts. A different digest must be reported; do not relabel it as the measured image.
2. Prepare the pinned external assets through the authors' documented flows, including matching Keys and stock F16 draft tensors, rank-cache format, RoPE/token map and local Engram. The public recipe describes that acquisition path; it does not certify a newly prepared asset tree.
3. Verify both rank launches, readiness, supported memory/thermal guards, normal Start/Stop and recovery under the operator's own container integration. This repository intentionally contains no machine-specific controller.
4. Bind the exact SparkDash collector source/version and local overlay to a public pin. The published method/settings and saved results are known, but the complete dashboard overlay is not part of this engine source closure.
5. Repeat only the two requested UI protocols, saving complete configurations, cached-token evidence and boundary counters. Keep capped speed observations separate from finished-answer quality or causal patch comparisons.

Publication static checks and source-patch verification should be recorded separately from model/runtime validation. Neither screenshots nor source review is a new runtime pass.
