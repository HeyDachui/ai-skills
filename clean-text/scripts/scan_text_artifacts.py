#!/usr/bin/env python3
"""Discover and clean promotional artifacts in line-oriented text files."""

from __future__ import annotations

import argparse
import codecs
import hashlib
import json
import os
import re
import tempfile
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


CUES = (
    "广告", "推广", "网站", "网址", "访问", "阅读", "下载", "更新", "最新",
    "最全", "推荐", "欢迎", "邮件", "邮箱", "地址", "联系", "上传", "分享",
    "论坛", "本站", "电子书", "版权所有",
)
SUFFIX_CUES = ("欢迎", "访问", "网址", "网站", "更多", "下载", "电子书", "光临")
WATERMARK_RE = re.compile(
    r"(?:电子书.*(?:制作|提供|下载|论坛|网站|上传|分享)|"
    r"(?:小说|全文|书籍).*(?:网站|论坛|下载|访问)|"
    r"(?:更多|最新|最全).*(?:小说|文章|电子书)|"
    r"请记住本站|备用网址|手机访问|电脑访问|版权所有)"
)
ADDRESS_RE = re.compile(
    r"(?:https?://|www\.)?[a-z0-9][a-z0-9-]*(?:\.[a-z0-9-]+)+"
    r"(?:/[a-z0-9._~:/?#\[\]@!$&'()*+,;=%-]*)?",
    re.IGNORECASE,
)
EMAIL_RE = re.compile(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", re.IGNORECASE)
CHAPTER_RE = re.compile(r"^\s*(?:第[〇零一二三四五六七八九十百千万0-9]+[章节卷回部篇]|卷[〇零一二三四五六七八九十百千万0-9]+)")


@dataclass(frozen=True)
class EncodingSpec:
    label: str
    codec: str
    bom: bytes = b""


ENCODINGS = {
    "utf-8": EncodingSpec("utf-8", "utf-8"),
    "utf-8-sig": EncodingSpec("utf-8-sig", "utf-8", codecs.BOM_UTF8),
    "gbk": EncodingSpec("gbk/cp936", "gbk"),
    "gb18030": EncodingSpec("gb18030", "gb18030"),
    "utf-16-le": EncodingSpec("utf-16-le", "utf-16-le", codecs.BOM_UTF16_LE),
    "utf-16-be": EncodingSpec("utf-16-be", "utf-16-be", codecs.BOM_UTF16_BE),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def detect_and_decode(raw: bytes, requested: str) -> tuple[str, EncodingSpec]:
    if requested != "auto":
        base = ENCODINGS[requested]
        preserved_bom = base.bom if base.bom and raw.startswith(base.bom) else b""
        spec = EncodingSpec(base.label, base.codec, preserved_bom)
        payload = raw[len(spec.bom):] if spec.bom and raw.startswith(spec.bom) else raw
        return payload.decode(spec.codec, errors="strict"), spec

    bom_specs = (
        (codecs.BOM_UTF8, ENCODINGS["utf-8-sig"]),
        (codecs.BOM_UTF16_LE, ENCODINGS["utf-16-le"]),
        (codecs.BOM_UTF16_BE, ENCODINGS["utf-16-be"]),
    )
    for bom, spec in bom_specs:
        if raw.startswith(bom):
            return raw[len(bom):].decode(spec.codec, errors="strict"), spec
    for key in ("utf-8", "gbk", "gb18030"):
        spec = ENCODINGS[key]
        try:
            return raw.decode(spec.codec, errors="strict"), spec
        except UnicodeDecodeError:
            pass
    raise UnicodeError("unable to decode input as UTF-8, GBK/CP936, GB18030, or BOM-marked UTF-16")


def encode_text(text: str, spec: EncodingSpec) -> bytes:
    return spec.bom + text.encode(spec.codec, errors="strict")


def normalized_with_map(value: str) -> tuple[str, list[int]]:
    chars: list[str] = []
    positions: list[int] = []
    for index, source_char in enumerate(value):
        expanded = unicodedata.normalize("NFKC", source_char).lower()
        for char in expanded:
            if char.isspace():
                continue
            if char in "。．":
                char = "."
            chars.append(char)
            positions.append(index)
    raw_view = "".join(chars)
    folded: list[str] = []
    folded_positions: list[int] = []
    index = 0
    while index < len(raw_view):
        if raw_view[index:index + 3] == "dot":
            folded.append(".")
            folded_positions.append(positions[index])
            index += 3
            continue
        if raw_view[index] == "点" and index + 2 < len(raw_view) and raw_view[index + 1:index + 3].isalpha():
            folded.append(".")
            folded_positions.append(positions[index])
            index += 1
            continue
        folded.append(raw_view[index])
        folded_positions.append(positions[index])
        index += 1
    return "".join(folded), folded_positions


def normalized(value: str) -> str:
    return normalized_with_map(value)[0]


def record(line_number: int, category: str, line: str, marker_hits: list[str], domain_hits: list[str], cue_hits: list[str], include_text: bool) -> dict[str, object]:
    item: dict[str, object] = {
        "line": line_number,
        "category": category,
        "text_sha256": sha256_text(line),
        "markers": marker_hits,
        "domains": domain_hits,
        "cues": cue_hits,
    }
    if include_text:
        item["text"] = line
    return item


def find_safe_suffix_strip(line: str, view: str, positions: list[int]) -> tuple[str, bool]:
    matches = list(ADDRESS_RE.finditer(view)) + list(EMAIL_RE.finditer(view))
    if not matches or not positions:
        return line, False
    address = max(matches, key=lambda item: item.end())
    tail = view[address.end():].strip("。.!！?？)）]】")
    if tail:
        return line, False
    punctuation_boundary = max((view.rfind(mark, 0, address.start()) for mark in ".。!！?？"), default=-1) + 1
    search_start = max(punctuation_boundary, address.start() - 60)
    cue_positions = [
        position
        for cue in SUFFIX_CUES
        for position in [view.find(cue, search_start, address.start())]
        if position >= 0
    ]
    cue_start = min(cue_positions, default=-1)
    if cue_start <= 0 or cue_start >= len(positions):
        return line, False
    original_start = positions[cue_start]
    prefix = line[:original_start].rstrip()
    if len(re.findall(r"[\u3400-\u9fff]", prefix)) < 6:
        return line, False
    return prefix, True


def classify_lines(lines: list[str], markers: list[str], domains: list[str], discover: bool, include_text: bool) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[int, str]]:
    views = [normalized(line) for line in lines]
    frequencies = Counter(view for view in views if view)
    planned: list[dict[str, object]] = []
    ambiguous: list[dict[str, object]] = []
    strips: list[dict[str, object]] = []
    strip_values: dict[int, str] = {}

    for index, (line, view) in enumerate(zip(lines, views), 1):
        mapped_view, positions = normalized_with_map(line)
        marker_hits = [item for item in markers if item and item in view]
        domain_hits = [item for item in domains if item and item in view]
        address_hits = list(ADDRESS_RE.finditer(view))
        email_hits = list(EMAIL_RE.finditer(view))
        cue_hits = [cue for cue in CUES if cue in view]
        watermark = bool(WATERMARK_RE.search(view))
        repeated_promo = frequencies[view] >= 3 and bool(cue_hits or address_hits or email_hits)
        supplied_combo = bool(marker_hits and (domain_hits or cue_hits or address_hits or email_hits))
        domain_combo = bool(domain_hits and (address_hits or email_hits or cue_hits))
        discovered_combo = discover and bool((address_hits or email_hits) and cue_hits)
        pure_address = discover and bool(address_hits or email_hits) and len(view) <= 100

        stripped, safe_strip = find_safe_suffix_strip(line, mapped_view, positions)
        if safe_strip and (discover or marker_hits or domain_hits):
            strips.append(record(index, "safe_suffix_strip", line, marker_hits, domain_hits, cue_hits, include_text))
            strip_values[index - 1] = stripped
            continue

        high_or_medium = supplied_combo or domain_combo or discovered_combo or watermark or repeated_promo
        if high_or_medium:
            planned.append(record(index, "planned_line_removal", line, marker_hits, domain_hits, cue_hits, include_text))
        elif marker_hits or domain_hits or pure_address:
            ambiguous.append(record(index, "ambiguous", line, marker_hits, domain_hits, cue_hits, include_text))

    return planned, strips, ambiguous, strip_values


def compact_summary(report: dict[str, object]) -> dict[str, object]:
    keys = (
        "mode", "encoding", "candidate_count", "planned_removal_count", "actual_removed_count",
        "planned_strip_count", "actual_stripped_fragment_count", "ambiguous_count",
        "residual_high_confidence_count", "source_unchanged", "chapter_headings_before",
        "chapter_headings_after", "delete_ratio", "output",
    )
    return {key: report.get(key) for key in keys if key in report}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--marker", action="append", default=[], help="Brand or stable text fragment; repeatable")
    parser.add_argument("--domain", action="append", default=[], help="Domain body or email-domain fragment; repeatable")
    parser.add_argument("--discover", action="store_true", help="Discover generic domains, emails, watermark language, and repeated promo lines")
    parser.add_argument("--encoding", choices=("auto", *ENCODINGS), default="auto")
    parser.add_argument("--apply", action="store_true", help="Write a cleaned copy")
    parser.add_argument("--output", type=Path, help="Required with --apply; must differ from input")
    parser.add_argument("--report", type=Path, help="Optional UTF-8 JSON report path")
    parser.add_argument("--include-text", action="store_true", help="Include full matched lines in the JSON report")
    parser.add_argument("--max-delete-ratio", type=float, default=0.25)
    parser.add_argument("--force", action="store_true", help="Allow replacing an existing output copy")
    args = parser.parse_args()

    if not args.discover and not args.marker and not args.domain:
        parser.error("provide --discover and/or at least one --marker or --domain")
    if args.apply and not args.output:
        parser.error("--output is required with --apply")
    if not 0 <= args.max_delete_ratio <= 1:
        parser.error("--max-delete-ratio must be between 0 and 1")
    if args.output and args.output.resolve() == args.input.resolve():
        parser.error("output must not overwrite input")
    if args.apply and args.output.exists() and not args.force:
        parser.error("output already exists; use --force to replace the output copy")

    raw = args.input.read_bytes()
    source_hash_before = sha256_bytes(raw)
    text, encoding = detect_and_decode(raw, args.encoding)
    newline = "\r\n" if "\r\n" in text else "\n"
    had_final_newline = text.endswith(("\n", "\r"))
    lines = text.splitlines()
    markers = [normalized(item) for item in args.marker]
    domains = [normalized(item).strip(".") for item in args.domain]
    planned, strips, ambiguous, strip_values = classify_lines(lines, markers, domains, args.discover, args.include_text)
    planned_indexes = {int(item["line"]) - 1 for item in planned}
    nonempty_count = max(1, sum(bool(line.strip()) for line in lines))
    delete_ratio = len(planned_indexes) / nonempty_count

    if args.apply and delete_ratio > args.max_delete_ratio:
        raise SystemExit(
            f"refusing to write: planned line deletion ratio {delete_ratio:.3f} exceeds "
            f"--max-delete-ratio {args.max_delete_ratio:.3f}"
        )

    actual_removed = 0
    actual_stripped = 0
    output_hash = None
    chapter_after = None
    residual_high = None
    output_replacement_chars = None

    if args.apply:
        output_lines: list[str] = []
        for index, line in enumerate(lines):
            if index in planned_indexes:
                actual_removed += 1
                continue
            if index in strip_values:
                output_lines.append(strip_values[index])
                actual_stripped += 1
            else:
                output_lines.append(line)
        output_text = newline.join(output_lines) + (newline if had_final_newline else "")
        output_bytes = encode_text(output_text, encoding)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=args.output.parent, prefix=args.output.name + ".", suffix=".tmp", delete=False) as handle:
            temp_path = Path(handle.name)
            handle.write(output_bytes)
        try:
            os.replace(temp_path, args.output)
        finally:
            if temp_path.exists():
                temp_path.unlink()

        verified_raw = args.output.read_bytes()
        verified_text, verified_encoding = detect_and_decode(verified_raw, args.encoding)
        if verified_encoding.label != encoding.label:
            raise RuntimeError("output encoding verification did not match the input encoding")
        output_hash = sha256_bytes(verified_raw)
        output_replacement_chars = verified_text.count("\ufffd")
        chapter_after = sum(bool(CHAPTER_RE.match(line)) for line in verified_text.splitlines())
        remaining_planned, _, _, _ = classify_lines(verified_text.splitlines(), markers, domains, args.discover, False)
        residual_high = len(remaining_planned)

    source_hash_after = sha256_bytes(args.input.read_bytes())
    report: dict[str, object] = {
        "input": str(args.input.resolve()),
        "input_sha256": source_hash_before,
        "mode": "apply" if args.apply else "scan",
        "encoding": encoding.label,
        "bom": bool(encoding.bom),
        "newline": "CRLF" if newline == "\r\n" else "LF",
        "output": str(args.output.resolve()) if args.apply else None,
        "output_sha256": output_hash,
        "candidate_count": len(planned) + len(strips) + len(ambiguous),
        "planned_removal_count": len(planned),
        "actual_removed_count": actual_removed,
        "planned_strip_count": len(strips),
        "actual_stripped_fragment_count": actual_stripped,
        "ambiguous_count": len(ambiguous),
        "residual_high_confidence_count": residual_high,
        "delete_ratio": round(delete_ratio, 6),
        "source_unchanged": source_hash_before == source_hash_after,
        "replacement_chars_before": text.count("\ufffd"),
        "replacement_chars_after": output_replacement_chars,
        "chapter_headings_before": sum(bool(CHAPTER_RE.match(line)) for line in lines),
        "chapter_headings_after": chapter_after,
        "planned_removals": planned,
        "planned_strips": strips,
        "ambiguous": ambiguous,
    }

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(compact_summary(report), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
