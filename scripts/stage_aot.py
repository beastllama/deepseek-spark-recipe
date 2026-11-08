"""Stage the pinned capacity kernels as a sibling of the selected kit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re

EXTENSION_SHA256 = "a3d107f687fa60c293afeb77629fe5d46c9d86ce3d5a9974d7c0a119badb87f9"
BASE_SHA256 = "29dccbcfdfc327a2ca83f40eb88c2bad83f9f61128e0cd27c29a1243d6fcd603"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read_extension():
    path = Path(__file__).with_name("AOT-CAPACITY-ROW-EXTENSION.json")
    data = path.read_bytes()
    need(sha(data) == EXTENSION_SHA256, "Published kernel binding differs")
    return json.loads(data)


def kernel_key(kernel):
    return (
        kernel["fn"],
        json.dumps(kernel["consts"], sort_keys=True),
        tuple((p["name"], p["type"], p["div16"], p["nospec"]) for p in kernel["params"]),
    )


def merge_manifest(base, extension):
    existing = base["kernels"]
    added = extension["kernels"]
    need(len(existing) == 198 and len(added) == 48, "Unexpected manifest size")
    need([k["consts"]["RB"]["int"] for k in added] == list(range(17, 65)), "Missing round rows")
    need(all(k["fn"] == "_rowmm_parts" for k in added), "Unexpected kernel function")
    old_keys = {kernel_key(k) for k in existing}
    add_keys = {kernel_key(k) for k in added}
    need(len(add_keys) == len(added) and not old_keys & add_keys, "Kernel variant collision")
    old_hashes = {k["hash"] for k in existing}
    add_hashes = {k["hash"] for k in added}
    need(len(add_hashes) == len(added) and not old_hashes & add_hashes, "Kernel identifier collision")
    return {**base, "kernels": existing + added}


def stage(base_kit, payload, candidate_kit):
    base_kit = base_kit.resolve(strict=True)
    payload = payload.resolve(strict=True)
    need(candidate_kit.name == "kit", "Candidate must be a kit directory")
    candidate_parent = candidate_kit.parent.resolve(strict=True)
    need(candidate_parent.parent == base_kit.parent.parent and candidate_parent != base_kit.parent,
         "Candidate parent must be a fresh sibling of the installed kit's parent")
    candidate = candidate_parent / "kit"
    need(not candidate.exists() and not candidate.is_symlink(), "Candidate already exists")
    extension = read_extension()
    original = (base_kit / "aot" / "aot.json").read_bytes()
    need(sha(original) == BASE_SHA256 == extension["base_manifest_sha256"], "Installed AOT preimage differs")
    old = json.loads(original)
    merged = merge_manifest(old, extension)
    existing = {}
    for kernel in old["kernels"]:
        identifier = kernel["hash"]
        need(re.fullmatch(r"[0-9a-f]{64}", identifier), "Invalid installed kernel identifier")
        name = identifier + ".cubin"
        path = base_kit / "aot" / "cubins" / name
        need(path.is_file(), "Installed kernel file missing: " + name)
        existing[name] = path
    binaries = {}
    for kernel, artifact in zip(extension["kernels"], extension["artifacts"], strict=True):
        name = kernel["hash"] + ".cubin"
        need(Path(artifact["path"]).name == name, "Published kernel filename differs")
        data = (payload / name).read_bytes()
        need(len(data) == artifact["size_bytes"] and sha(data) == artifact["sha256"],
             "Published kernel bytes differ: " + name)
        need(data[:4] == b"\x7fELF" and data[18:20] == b"\xbe\x00",
             "Expected an NVIDIA CUDA ELF kernel: " + name)
        binaries[name] = data
    need(sum(map(len, binaries.values())) == extension["total_bytes"], "Kernel payload total differs")

    candidate.mkdir(mode=0o700)
    aot = candidate / "aot"
    cubins = aot / "cubins"
    cubins.mkdir(parents=True, mode=0o700)
    for child in base_kit.iterdir():
        if child.name not in {"aot", "MANIFEST"}:
            (candidate / child.name).symlink_to(
                os.path.relpath(child, candidate), target_is_directory=child.is_dir())
    for name, path in existing.items():
        (cubins / name).symlink_to(os.path.relpath(path, cubins))
    for name, data in binaries.items():
        with (cubins / name).open("xb") as output:
            output.write(data)
    manifest = (json.dumps(merged, indent=1) + "\n").encode()
    with (aot / "aot.json").open("xb") as output:
        output.write(manifest)
    return {"candidate_kit": str(candidate), "base_aot_sha256": BASE_SHA256,
            "aot_sha256": sha(manifest), "preserved": len(old["kernels"]), "added": len(binaries)}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("base_kit", type=Path)
    cli.add_argument("verified_cubins_directory", type=Path)
    cli.add_argument("candidate_kit", type=Path)
    args = cli.parse_args()
    print(json.dumps(stage(args.base_kit, args.verified_cubins_directory, args.candidate_kit)))


if __name__ == "__main__":
    main()

