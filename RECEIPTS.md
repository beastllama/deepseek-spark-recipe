# Publication verification receipts

The publication preparation performed source and static checks only. It did not build a model runtime, acquire model assets, start/stop a model or generate tokens. The original runtime build evidence and benchmark numbers remain separate in [build-identity.json](data/build-identity.json) and [results.json](data/results.json).

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

Machine-readable receipt: [publication-checks.json](data/publication-checks.json). The recipe has no package manifest or typecheck/build task of its own; shell/Python/JSON static checks were performed. A clean ARM64 Docker build and a runtime trial of this packaging remain unexecuted, as described in [REPRODUCTION-STATUS.md](REPRODUCTION-STATUS.md).
