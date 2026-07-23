#!/usr/bin/env python3
import argparse, hashlib, json
from collections import Counter
from pathlib import Path

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def nested(data, *paths):
    for path in paths:
        cur = data
        for key in path:
            if not isinstance(cur, dict) or key not in cur:
                break
            cur = cur[key]
        else:
            return cur
    return None

def audit(queue_path, reports_dir):
    queue = json.loads(Path(queue_path).read_text(encoding="utf-8-sig"))
    records = queue.get("records", queue if isinstance(queue, list) else [])
    issues, items = [], []
    ids, targets = Counter(), Counter()
    for r in records:
        job = str(r.get("combo_job_id") or r.get("job_id") or "")
        target = Path(r.get("target_path", "")) if r.get("target_path") else None
        receipt_path = Path(r.get("receipt_path") or (Path(reports_dir) / f"{job}.json"))
        ids[job] += 1
        if target: targets[str(target).lower()] += 1
        image_exists = bool(target and target.is_file())
        receipt = None
        if receipt_path.is_file():
            try:
                receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
            except Exception as exc:
                issues.append({"job_id": job, "code": "invalid_receipt_json", "detail": str(exc)})
        generation_status = nested(receipt or {}, ("generation_status",), ("production_status",),
                                   ("generation_audit", "generation_status"))
        retry_allowed = nested(receipt or {}, ("retry_allowed",), ("generation_audit", "retry_allowed"),
                               ("generation_error", "retry_allowed"), ("generation_audit", "retry", "retry_allowed"))
        if generation_status is None and nested(receipt or {}, ("generation_audit", "moderation_blocked")) is True:
            generation_status = "moderation_blocked"
        terminal_block = generation_status == "moderation_blocked" and retry_allowed is False
        network_retry_count = nested(receipt or {}, ("network_retry_count",),
                                     ("generation_audit", "network_retry_count"),
                                     ("generation_audit", "retry", "count")) or 0
        receipt_status = nested(receipt or {}, ("status",), ("visual_qa", "status"),
                                ("visual_acceptance", "status"))
        if receipt:
            receipt_job = receipt.get("combo_job_id") or receipt.get("job_id")
            if receipt_job and receipt_job != job:
                issues.append({"job_id": job, "code": "receipt_job_mismatch", "actual": receipt_job})
            receipt_target = nested(receipt, ("target_path",), ("generation_audit", "target_path"))
            if target and receipt_target and Path(receipt_target) != target:
                issues.append({"job_id": job, "code": "target_path_mismatch", "actual": receipt_target})
        if image_exists and receipt:
            expected_size = nested(receipt, ("result_bytes",), ("generation_audit", "result_bytes"))
            expected_hash = nested(receipt, ("result_sha256",), ("generation_audit", "result_sha256"))
            if expected_size is not None and target.stat().st_size != int(expected_size):
                issues.append({"job_id": job, "code": "size_mismatch"})
            if expected_hash and sha256(target).lower() != str(expected_hash).lower():
                issues.append({"job_id": job, "code": "hash_mismatch"})
            receipt_prompt = nested(receipt, ("actual_final_prompt",), ("generation_audit", "actual_final_prompt"))
            if receipt_prompt and r.get("actual_final_prompt") and receipt_prompt != r["actual_final_prompt"]:
                issues.append({"job_id": job, "code": "prompt_mismatch"})
        if image_exists and not receipt:
            issues.append({"job_id": job, "code": "image_without_receipt"})
        if receipt and not image_exists and not terminal_block:
            code = "network_failure_no_image" if receipt_status == "pending_network_retry" or network_retry_count else "receipt_without_image"
            issues.append({"job_id": job, "code": code, "network_retry_count": network_retry_count})
        items.append({"job_id": job, "queue_status": r.get("status"), "image_exists": image_exists,
                      "receipt_exists": receipt is not None, "terminal_block": terminal_block})
    for value, count in ids.items():
        if not value or count > 1: issues.append({"job_id": value, "code": "duplicate_or_empty_job_id", "count": count})
    for value, count in targets.items():
        if count > 1: issues.append({"target_path": value, "code": "duplicate_target_path", "count": count})
    return {
        "schema": "batch-image-production-audit/v1",
        "queue": str(Path(queue_path).resolve()),
        "total": len(records),
        "local_images": sum(x["image_exists"] for x in items),
        "receipts": sum(x["receipt_exists"] for x in items),
        "terminal_blocks": sum(x["terminal_block"] for x in items),
        "queue_statuses": dict(Counter(str(x["queue_status"]) for x in items)),
        "issue_counts": dict(Counter(x["code"] for x in issues)),
        "issues": issues,
        "items": items,
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--queue", required=True)
    p.add_argument("--reports-dir", required=True)
    p.add_argument("--output")
    a = p.parse_args()
    result = audit(a.queue, a.reports_dir)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if a.output:
        output = Path(a.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("total", "local_images", "receipts", "terminal_blocks", "issue_counts")}, ensure_ascii=False))
