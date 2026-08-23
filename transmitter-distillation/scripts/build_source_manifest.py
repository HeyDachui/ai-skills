#!/usr/bin/env python3
"""Build a portable source manifest for books, papers, and creative works.

Usage:
  python build_source_manifest.py --input ./materials --output ./source_manifest.json

The script records the paths supplied by the caller. It does not assume any
drive, workspace, catalog, or operating-system-specific directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def collect(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    if not root.is_dir():
        raise FileNotFoundError(root)
    return sorted(p for p in root.rglob("*") if p.is_file())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="A source file or directory")
    parser.add_argument("--output", required=True, help="Manifest JSON path")
    parser.add_argument("--subject", default="", help="Optional research subject")
    args = parser.parse_args()

    root = Path(args.input).expanduser()
    rows = []
    for path in collect(root):
        rows.append(
            {
                "source_id": f"SRC-{len(rows) + 1:03d}",
                "source_ref": str(path),
                "name": path.name,
                "media_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )

    payload = {
        "schema": "transmitter.source_manifest.v1",
        "subject": args.subject,
        "sources": rows,
    }
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "sources": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
