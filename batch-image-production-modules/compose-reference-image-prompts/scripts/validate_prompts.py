#!/usr/bin/env python3
import argparse, json
from collections import Counter
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--queue", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--required-phrase", action="append", default=[])
    p.add_argument("--forbidden-phrase", action="append", default=[])
    a = p.parse_args()
    data = json.loads(Path(a.queue).read_text(encoding="utf-8-sig"))
    records = data.get("records", data if isinstance(data, list) else [])
    rows = []
    for r in records:
        job = r.get("combo_job_id") or r.get("job_id")
        prompt = str(r.get("actual_final_prompt") or "")
        issues = []
        if not prompt.strip(): issues.append("missing_prompt")
        for phrase in a.required_phrase:
            if phrase not in prompt: issues.append(f"missing_required:{phrase}")
        for phrase in a.forbidden_phrase:
            if phrase.lower() in prompt.lower(): issues.append(f"contains_forbidden:{phrase}")
        if len(prompt.strip()) < 40: issues.append("prompt_too_short")
        rows.append({"job_id": job, "characters": len(prompt), "issues": issues})
    result = {"schema": "reference-prompt-validation/v1", "total": len(rows),
              "valid": sum(not r["issues"] for r in rows),
              "issue_counts": dict(Counter(x for r in rows for x in r["issues"])),
              "records": rows}
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("total","valid","issue_counts")}, ensure_ascii=False))
if __name__ == "__main__": main()
