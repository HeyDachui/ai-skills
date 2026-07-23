#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--queue", required=True)
    p.add_argument("--plan", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--workers", type=int, default=3)
    p.add_argument("--max-network-retries", type=int, default=1)
    a = p.parse_args()
    queue_data = json.loads(Path(a.queue).read_text(encoding="utf-8-sig"))
    records = queue_data.get("records", queue_data if isinstance(queue_data, list) else [])
    by_id = {str(r.get("combo_job_id") or r.get("job_id")): r for r in records}
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8-sig"))
    jobs = [x["job_id"] for batch in plan.get("batches", []) for x in batch]
    missing = [j for j in jobs if j not in by_id]
    if missing: raise SystemExit(f"Plan contains unknown job IDs: {missing[:5]}")
    output = Path(a.output_dir); output.mkdir(parents=True, exist_ok=True)
    packets = [[] for _ in range(max(1, a.workers))]
    skipped = []
    for index, job in enumerate(jobs):
        r = by_id[job]; target = Path(r.get("target_path", ""))
        if target.is_file():
            skipped.append({"job_id": job, "reason": "target_exists"}); continue
        packets[index % len(packets)].append({
            "job_id": job,
            "reference_path": r.get("outfit_reference_path") or r.get("reference_path"),
            "actual_final_prompt": r.get("actual_final_prompt"),
            "target_path": r.get("target_path"),
            "receipt_path": r.get("receipt_path"),
            "max_network_retries": a.max_network_retries,
        })
    manifest = []
    for i, jobs_for_worker in enumerate(packets, 1):
        packet = {"schema": "image-generation-worker-packet/v1", "worker_number": i,
                  "autonomous_continuation_allowed": False,
                  "return_embedded_image_or_base64": False, "jobs": jobs_for_worker}
        path = output / f"worker_{i:02d}.json"
        path.write_text(json.dumps(packet, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        manifest.append({"worker_number": i, "packet": str(path.resolve()), "jobs": len(jobs_for_worker)})
    (output/"dispatch_manifest.json").write_text(json.dumps({"packets": manifest,"skipped": skipped},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"workers": len(packets), "dispatched": sum(len(x) for x in packets), "skipped": len(skipped)}, ensure_ascii=False))
if __name__ == "__main__": main()
