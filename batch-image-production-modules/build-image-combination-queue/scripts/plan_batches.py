#!/usr/bin/env python3
import argparse, json
from collections import defaultdict, deque
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--queue", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--batch-size", type=int, default=12)
    p.add_argument("--max-per-group", type=int, default=3)
    p.add_argument("--exclude-term", action="append", default=[])
    p.add_argument("--reports-dir")
    p.add_argument("--max-network-retries", type=int, default=1)
    a = p.parse_args()
    data = json.loads(Path(a.queue).read_text(encoding="utf-8-sig"))
    records = data.get("records", data if isinstance(data, list) else [])
    groups = defaultdict(list)
    excluded = []
    for r in sorted(records, key=lambda x: x.get("queue_number", 10**12)):
        target = Path(r.get("target_path", "")) if r.get("target_path") else None
        haystack = " ".join(str(r.get(k, "")) for k in ("actual_final_prompt", "outfit_master_id", "group_id")).lower()
        reason = None
        job = r.get("combo_job_id") or r.get("job_id")
        receipt_path = Path(r.get("receipt_path") or (Path(a.reports_dir) / f"{job}.json")) if a.reports_dir else None
        receipt = {}
        if receipt_path and receipt_path.is_file():
            try: receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
            except Exception: receipt = {}
        generation_status = receipt.get("generation_status") or receipt.get("production_status") or receipt.get("generation_audit", {}).get("generation_status")
        retry_allowed = receipt.get("retry_allowed")
        if retry_allowed is None: retry_allowed = receipt.get("generation_audit", {}).get("retry_allowed")
        if retry_allowed is None: retry_allowed = receipt.get("generation_error", {}).get("retry_allowed")
        if retry_allowed is None: retry_allowed = (receipt.get("generation_audit") or {}).get("retry") or {}
        if isinstance(retry_allowed, dict): retry_allowed = retry_allowed.get("retry_allowed")
        if generation_status is None and receipt.get("generation_audit", {}).get("moderation_blocked") is True:
            generation_status = "moderation_blocked"
        network_retry_count = (receipt.get("generation_audit") or {}).get("network_retry_count") or 0
        receipt_status = receipt.get("status") or (receipt.get("visual_qa") or {}).get("status")
        if generation_status == "moderation_blocked" and retry_allowed is False: reason = "terminal_moderation_block"
        elif receipt_status == "pending_network_retry" and int(network_retry_count) >= a.max_network_retries: reason = "network_retry_exhausted"
        elif r.get("status") in {"blocked", "excluded", "moderation_blocked"}: reason = "terminal_status"
        elif target and target.is_file(): reason = "target_exists"
        elif any(term.lower() in haystack for term in a.exclude_term): reason = "excluded_term"
        if reason:
            excluded.append({"job_id": job, "reason": reason})
            continue
        group = str(r.get("outfit_master_id") or r.get("group_id") or "ungrouped")
        groups[group].append(r)
    queues = {k: deque(v) for k, v in groups.items()}
    batches = []
    while any(queues.values()):
        batch, counts = [], defaultdict(int)
        while len(batch) < a.batch_size:
            candidates = [g for g, q in queues.items() if q and counts[g] < a.max_per_group]
            if not candidates: break
            candidates.sort(key=lambda g: (counts[g], -len(queues[g]), g))
            group = candidates[0]
            used_families = {x.get("action_family_id") for x in batch if x.get("_group") == group}
            idx = next((i for i, x in enumerate(queues[group]) if x.get("action_family_id") not in used_families), 0)
            queues[group].rotate(-idx); record = queues[group].popleft(); queues[group].rotate(idx)
            batch.append({"job_id": record.get("combo_job_id") or record.get("job_id"),
                          "group_id": group, "variation_id": record.get("action_family_id"),
                          "queue_number": record.get("queue_number"), "_group": group})
            counts[group] += 1
        for x in batch: x.pop("_group", None)
        if not batch: break
        batches.append(batch)
    output = {"schema": "batch-image-dispatch-plan/v1", "batch_size": a.batch_size,
              "max_per_group": a.max_per_group, "batches": batches, "excluded": excluded}
    output_path = Path(a.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"batches": len(batches), "planned": sum(map(len, batches)), "excluded": len(excluded)}, ensure_ascii=False))
if __name__ == "__main__": main()
