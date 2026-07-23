#!/usr/bin/env python3
import argparse, json
from collections import Counter, defaultdict
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--queue", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--preferred-visible-per-group", type=int, default=5)
    a = p.parse_args()
    data = json.loads(Path(a.queue).read_text(encoding="utf-8-sig"))
    records = data.get("records", data if isinstance(data, list) else [])
    groups = defaultdict(list)
    for r in sorted(records, key=lambda x: x.get("queue_number", 10**12)):
        target = Path(r.get("target_path", "")) if r.get("target_path") else None
        if target and target.is_file():
            group = str(r.get("outfit_master_id") or r.get("group_id") or "ungrouped")
            groups[group].append({"job_id": r.get("combo_job_id") or r.get("job_id"),
                                  "queue_number": r.get("queue_number"),
                                  "variation_id": r.get("action_family_id"),
                                  "image_path": str(target)})
    report = []
    for group, items in sorted(groups.items(), key=lambda x: (-len(x[1]), x[0])):
        report.append({"group_id": group, "image_count": len(items),
                       "over_preferred_limit": max(0, len(items)-a.preferred_visible_per_group),
                       "distinct_variations": len(set(x["variation_id"] for x in items)),
                       "review_candidates_after_preferred_limit": items[a.preferred_visible_per_group:],
                       "items": items})
    result = {"schema": "image-diversity-analysis/v1", "local_images": sum(len(x) for x in groups.values()),
              "groups": len(groups), "preferred_visible_per_group": a.preferred_visible_per_group,
              "groups_over_limit": sum(x["over_preferred_limit"] > 0 for x in report),
              "review_candidates": sum(x["over_preferred_limit"] for x in report),
              "analysis": report,
              "note": "Candidates require human review; this file does not hide or delete images."}
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("local_images","groups","groups_over_limit","review_candidates")}, ensure_ascii=False))
if __name__ == "__main__": main()
