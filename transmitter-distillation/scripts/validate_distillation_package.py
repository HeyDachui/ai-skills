#!/usr/bin/env python3
"""Validate a transmitter-distillation candidate package.

Usage:
  python validate_distillation_package.py --manifest source_manifest.json \
      --cards distillation_cards.jsonl

This is a deterministic structural check. It cannot decide whether an
interpretation is insightful, whether a source is licensed, or whether a style
profile works in real production.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REQUIRED = {
    "schema",
    "card_id",
    "title",
    "kind",
    "problem",
    "source_observations",
    "ai_interpretation",
    "transferable_mechanism",
    "boundaries",
    "attribution",
    "evidence_records",
    "reading_scope",
    "status",
}


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_no}: row must be an object")
        rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--cards", required=True)
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    source_ids = {row["source_id"] for row in manifest.get("sources", [])}
    cards = load_jsonl(Path(args.cards))
    ids = set()
    evidence_count = 0
    errors = []

    for index, card in enumerate(cards, start=1):
        missing = REQUIRED - set(card)
        if missing:
            errors.append(f"card {index} missing: {sorted(missing)}")
        card_id = card.get("card_id")
        if card_id in ids:
            errors.append(f"duplicate card_id: {card_id}")
        ids.add(card_id)
        if card.get("status") != "candidate_only_not_adopted_effect_unknown":
            errors.append(f"card {card_id}: invalid candidate status")
        if not isinstance(card.get("source_observations"), list) or not card["source_observations"]:
            errors.append(f"card {card_id}: source_observations must be non-empty")
        for evidence in card.get("evidence_records", []):
            evidence_count += 1
            source_id = evidence.get("source_id")
            if source_id not in source_ids:
                errors.append(f"card {card_id}: unknown evidence source {source_id}")
            excerpt = evidence.get("excerpt", "")
            if not excerpt.strip():
                errors.append(f"card {card_id}: empty evidence excerpt")
            actual = hashlib.sha256(excerpt.encode("utf-8")).hexdigest()
            if evidence.get("excerpt_sha256") != actual:
                errors.append(f"card {card_id}: excerpt_sha256 mismatch")
        if not card.get("evidence_records"):
            errors.append(f"card {card_id}: no evidence_records")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    print(json.dumps({"status": "PASS", "cards": len(cards), "evidence_records": evidence_count}, ensure_ascii=False))


if __name__ == "__main__":
    main()
