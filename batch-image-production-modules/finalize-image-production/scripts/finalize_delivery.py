#!/usr/bin/env python3
import argparse, json, shutil
from pathlib import Path
from audit_production import audit

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--queue", required=True)
    p.add_argument("--reports-dir", required=True)
    p.add_argument("--output-dir", required=True)
    a = p.parse_args()
    out = Path(a.output_dir); out.mkdir(parents=True, exist_ok=True)
    data = json.loads(Path(a.queue).read_text(encoding="utf-8-sig"))
    records = data.get("records", data if isinstance(data, list) else [])
    audit_result = audit(a.queue, a.reports_dir)
    index, prompts = [], []
    for r in sorted(records, key=lambda x: x.get("queue_number", 10**12)):
        target = Path(r.get("target_path", "")) if r.get("target_path") else None
        if not target or not target.is_file(): continue
        job = r.get("combo_job_id") or r.get("job_id")
        row = {"number": len(index)+1, "job_id": job, "image_path": str(target.resolve()),
               "group_id": r.get("outfit_master_id") or r.get("group_id"),
               "variation_id": r.get("action_family_id"), "prompt": r.get("actual_final_prompt", "")}
        index.append(row); prompts.append(row)
    (out/"IMAGE_INDEX.json").write_text(json.dumps(index, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    with (out/"IMAGE_PROMPTS.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for row in prompts: f.write(json.dumps(row, ensure_ascii=False)+"\n")
    with (out/"ALL_IMAGE_PROMPTS_PLAIN.txt").open("w", encoding="utf-8-sig", newline="\n") as f:
        for i, row in enumerate(prompts, 1):
            if i > 1: f.write("\n"+"="*60+"\n\n")
            f.write(f"第{i}张\n\n{row['prompt'].strip()}\n")
    summary = {k: audit_result[k] for k in ("total","local_images","receipts","terminal_blocks","queue_statuses","issue_counts")}
    (out/"AUDIT_SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    report = ["# 批量图片生产最终报告","",f"- 队列总数：{summary['total']}",f"- 本地图片：{summary['local_images']}",
              f"- 回执数量：{summary['receipts']}",f"- 不可重试拦截：{summary['terminal_blocks']}",
              f"- 未解决问题：{sum(summary['issue_counts'].values())}","", "## 问题分布","",
              "```json",json.dumps(summary["issue_counts"],ensure_ascii=False,indent=2),"```",""]
    (out/"FINAL_REPORT.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"output_dir": str(out.resolve()), "images": len(index), "issues": sum(summary["issue_counts"].values())}, ensure_ascii=False))
if __name__ == "__main__": main()
