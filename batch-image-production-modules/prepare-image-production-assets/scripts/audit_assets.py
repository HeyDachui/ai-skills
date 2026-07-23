#!/usr/bin/env python3
import argparse, json
from collections import Counter
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--queue", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    data = json.loads(Path(a.queue).read_text(encoding="utf-8-sig"))
    records = data.get("records", data if isinstance(data, list) else [])
    ids = Counter(str(r.get("combo_job_id") or r.get("job_id") or "") for r in records)
    targets = Counter(str(r.get("target_path") or "").lower() for r in records)
    ready, blocked = [], []
    for r in records:
        job = str(r.get("combo_job_id") or r.get("job_id") or "")
        reference = r.get("outfit_reference_path") or r.get("reference_path")
        target = str(r.get("target_path") or "")
        reasons = []
        if not job or ids[job] > 1: reasons.append("blocked_ambiguous_identity")
        if not target or targets[target.lower()] > 1: reasons.append("blocked_ambiguous_target")
        if not reference or not Path(reference).is_file(): reasons.append("blocked_missing_reference")
        if not str(r.get("actual_final_prompt") or "").strip(): reasons.append("blocked_missing_prompt")
        row = {"job_id": job, "reference_path": reference, "target_path": target}
        if reasons:
            row["reasons"] = sorted(set(reasons)); blocked.append(row)
        else:
            ready.append(row)
    result = {"schema": "image-asset-readiness/v1", "total": len(records),
              "ready": ready, "blocked": blocked,
              "blocked_reasons": dict(Counter(x for r in blocked for x in r["reasons"]))}
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"total": len(records), "ready": len(ready), "blocked": len(blocked),
                      "blocked_reasons": result["blocked_reasons"]}, ensure_ascii=False))
if __name__ == "__main__": main()
