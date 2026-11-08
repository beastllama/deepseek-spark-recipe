# Publication verification receipts

The publication preparation performed source and static checks only. It did not build a model runtime, acquire model assets, start/stop a model or generate tokens. The original runtime build evidence and benchmark numbers remain separate in [build-identity-v0.1.json](data/build-identity-v0.1.json) and [results.json](data/results.json).

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

The v0.1 patch and original result export are unchanged. Its manifest, build identity and publication checks are retained with `-v0.1` names. The current manifest/build identity describe full-prefix image `efceb406…`, not a rerun of the historical 311.10/2,232.53 observations.

A fresh Linux directory was populated from the saved public `fbbc97132cd004237d9887b8d3185896efaedc5c` archive. Each patch passed `git apply --check` and then applied in order. Exact source hashes were verified after each step:

| Patch | Resulting 1,117-file closure |
| --- | --- |
| `tested-stack.patch` | `4df32ee4fc221d4e773542005750fd4fa411deed331ab2d8218fab5785eb85ce` |
| `cache-cut-in.patch` | `c3d01df87896197e3f67e1ba06cf85992987d05ed3f4cc4d72dc17594cf3da04` |
| `full-prefix-backing.patch` | `e6581809b03c00c99f79f090ee4891dda0f3ee1b7bbb0159b78f8d2454a80b8c` |

The existing verifier passed with the historical manifest after step one and with the default current manifest after step three. The final source contains 1,117 files / 9,878,200 bytes. [patch-series.json](data/patch-series.json) binds all patch and changed-file hashes. The unchanged public base plus the ordered patches reconstructs the recorded v0.2 source; this does not establish binary equivalence.

The current publication receipt records shell syntax, Python syntax/import checks, JSON parsing, manifest/inventory consistency, numeric calculation checks and a bounded privacy-pattern scan. The repository has no package manifest or standalone typecheck/build task; source reconstruction and static script checks are the appropriate package checks. No ARM64 model build, asset installation, screen access, live workload read, generation or benchmark was performed for this update. The saved local native rebuild passed with retained GPU bundles; clean public ARM64/GPU reproduction remains unverified.

Current machine-readable receipt: [publication-checks.json](data/publication-checks.json).
