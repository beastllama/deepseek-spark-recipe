# Publication verification receipts

The original publication preparation performed source and static checks only. It did not build a model runtime, acquire model assets, start/stop a model or generate tokens. Later recency trial qualification is recorded separately below. The original runtime build evidence and benchmark numbers remain separate in [build-identity-v0.1.json](data/build-identity-v0.1.json) and [results.json](data/results.json).

On November 7, 2026, the exact source-only export contained **1,117 files / 9,872,803 bytes**. It was compared with the public source archive for TensorFold `fbbc97132cd004237d9887b8d3185896efaedc5c`. The produced patch contains 53 modified files and seven additions; its SHA-256 is:

```text
3da4edaff9df6dee1183b89ce644448a88715774adb5b342be13926453db073a
```

The source archive was read without extracting its Windows-incompatible fixture names onto NTFS. A fresh Linux directory received the unmodified public files in the recorded closure. Both commands exited 0 there:

```sh
git apply --check /path/to/recipe/patches/tested-stack.patch
git apply /path/to/recipe/patches/tested-stack.patch
```

The actual verifier then ran against that reconstructed directory:

```sh
python3 /path/to/recipe/scripts/verify-source.py /path/to/reconstructed-source
```

Observed output:

```json
{"source_files": 1117, "source_tree_sha256": "4df32ee4fc221d4e773542005750fd4fa411deed331ab2d8218fab5785eb85ce"}
```

`bash -n scripts/launch-rank.sh` exited 0. Python's AST parser accepted both published Python scripts, and the JSON parser accepted all JSON files. The original `stage_aot.py` helper's `read_extension()` verified its sealed extension file; the manifest contains 48 kernel/artifact pairs for rows 17–64, totaling 18,795,792 bytes. No cubin payload was fetched or executed by these checks.

A bounded scan of the public text files found no recorded private host names/paths, known private addresses, Hugging Face/GitHub token-shaped strings or private-key headers. Public authors' attribution names and public asset references remain. This scan complements source review; it does not claim comprehensive secret detection.

Historical machine-readable receipt: [publication-checks-v0.1.json](data/publication-checks-v0.1.json). The recipe has no package manifest or typecheck/build task of its own; shell/Python/JSON static checks were performed. A clean ARM64 Docker build and a runtime trial of this packaging remain unexecuted, as described in [REPRODUCTION-STATUS.md](REPRODUCTION-STATUS.md).

## November 8 v0.2 source-preview verification

The v0.1 patch and original result export are unchanged. Its manifest, build identity and publication checks are retained with `-v0.1` names. The published v0.2 manifest and build identity describe full-prefix image `efceb406…`. The `-v0.2` files preserve those original identities alongside the v0.3.0 recency source preview.

A fresh Linux directory was populated from the saved public `fbbc97132cd004237d9887b8d3185896efaedc5c` archive. Each patch passed `git apply --check` and then applied in order. Exact source hashes were verified after each step:

| Patch | Resulting 1,117-file closure |
| --- | --- |
| `tested-stack.patch` | `4df32ee4fc221d4e773542005750fd4fa411deed331ab2d8218fab5785eb85ce` |
| `cache-cut-in.patch` | `c3d01df87896197e3f67e1ba06cf85992987d05ed3f4cc4d72dc17594cf3da04` |
| `full-prefix-backing.patch` | `e6581809b03c00c99f79f090ee4891dda0f3ee1b7bbb0159b78f8d2454a80b8c` |

The existing verifier passed with the historical manifest after step one and with the then-default v0.2 manifest after step three. That v0.2 source contains 1,117 files / 9,878,200 bytes. [The archived v0.2 manifest](data/source-manifest-v0.2.json) preserves its exact hashes. The unchanged public base plus those first three ordered patches reconstructs the recorded v0.2 source; this does not establish binary equivalence.

The v0.2 publication receipt records shell syntax, Python syntax/import checks, JSON parsing, manifest/inventory consistency, numeric calculation checks and a bounded privacy-pattern scan. The repository has no package manifest or standalone typecheck/build task; source reconstruction and static script checks are the appropriate package checks. No ARM64 model build, asset installation, screen access, live workload read, generation or benchmark was performed for that publication update. The saved local native rebuild passed with retained GPU bundles; clean public ARM64/GPU reproduction remains unverified.

Historical v0.2 machine-readable receipt: [publication-checks-v0.2.json](data/publication-checks-v0.2.json).

## Recency source verification and actual trial qualification

The fourth ordered `prefix-recency.patch` changes only the compact Store's superseded preference in `zig/src/core/prompt_cache.zig`: preimage `c25bcb27b5c095b251d348cd8506229c32ef1788e260700b43e5b236c904180e`, postimage `8210b249ee4f66000b2ecb4dd9b6c376dbcdf3eb66b2e275d14677f38e9e9130`. A fresh reconstruction from the saved public archive passed all four `git apply --check` and application steps, then the existing source verifier. Its final 1,117 files / 9,878,221 bytes have closure `aa0f3dcdda5da77c13debb69ad4ac4fe1549518af54925ec3e7b80ab8441a041`. The historical v0.2 manifest correctly rejects that changed core. [patch-series.json](data/patch-series.json) and the current manifest bind the candidate; the earlier three patch bytes and historical results remain unchanged.

Offline patch application and source checks have their own receipt. The controller accepted the trial qualification at epoch 1794180235.343796, before the trial deadline of 1794180310.4231122. The qualification receipt has SHA-256 `d366a7825e4d4c85db21694af3e3b74f9c27491e965625074442b903523541b1` and records `selected=false` for the original trial. The saved evidence binds the ten-request SparkDash retention job and one 32K Native Quality control to the qualified artifacts through receipt digests. [Offline checks](data/publication-checks.json) · [Sanitized job and source evidence](data/recency-results.json).

The saved trial qualified the artifacts with 10/10 correct retention requests and 16/16 keys recovered without stale values. It closed through normal fallback after cross-host timestamp and commit-margin guards prevented selection. A separate observation at 2026-11-08 23:51:13.779361 UTC confirmed persistent selection and readiness of the identical image, source, binaries and settings. Both memory guards, exact bindings and normal timers were verified. The adoption used the original qualification and zero additional benchmark jobs or inference requests. [Qualification, artifact equivalence, startup and selection receipt digests](data/recency-results.json).

The saved candidate compiler proof is successful, with retained GPU bundles, while the original overall build observation remains failed because the existing memory watchdog interrupted the serving pair. A later observation confirmed that cause, and the compiled payload received separate COPY-only acceptance. The source/build identity retains that distinction and both required head/worker memory guards. The subsequent narrow UI qualification does not erase the original continuity failure, establish a clean public ARM64/GPU rebuild or prove binary equivalence. It is not a matched GPU speedup, broad quality or whole-project result.
