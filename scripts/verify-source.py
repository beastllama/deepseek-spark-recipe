#!/usr/bin/env python3
"""Verify the recorded native source closure (v0.2 by default)."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("source", type=Path)
    cli.add_argument("--manifest", type=Path,
                     help="Use an explicit historical source manifest")
    args = cli.parse_args()
    manifest_path = args.manifest or Path(__file__).resolve().parents[1] / "data" / "source-manifest.json"
    expected = json.loads(manifest_path.read_text())
    actual = {}
    for name, wanted in expected["manifest"].items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise SystemExit("Invalid manifest path: " + name)
        path = args.source / relative
        if path.is_symlink() or not path.is_file():
            raise SystemExit("Missing or nonregular source: " + name)
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        if got != wanted:
            raise SystemExit("Source differs: " + name)
        actual[name] = got
    closure = hashlib.sha256(json.dumps(actual, sort_keys=True).encode()).hexdigest()
    if closure != expected["source_tree_sha256"]:
        raise SystemExit("Source closure digest differs")
    print(json.dumps({"source_files": len(actual), "source_tree_sha256": closure}))


if __name__ == "__main__":
    main()
