#!/usr/bin/env python3
"""Extract PDF pages with stable page markers.

Requires the optional `pypdf` package. The output is a navigation aid, not a
replacement for reading承重 pages or preserving the original PDF.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="PDF file")
    parser.add_argument("--output", required=True, help="UTF-8 text output")
    args = parser.parse_args()
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit("Missing optional dependency: install pypdf, then rerun this script.") from exc

    pdf = Path(args.input).expanduser()
    if not pdf.is_file():
        raise SystemExit(f"Input PDF does not exist: {pdf}")
    reader = PdfReader(str(pdf))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"--- PAGE {index} ---\n{text.rstrip()}\n")

    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(pages), encoding="utf-8")
    print(f"extracted_pages={len(reader.pages)} output={output}")


if __name__ == "__main__":
    main()
