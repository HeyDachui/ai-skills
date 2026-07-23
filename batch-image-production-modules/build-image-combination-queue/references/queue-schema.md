# Queue schema

Minimum portable fields:

```json
{
  "job_id": "stable unique value",
  "queue_number": 1,
  "group_id": "outfit or other visual group",
  "action_family_id": "variation family",
  "actual_final_prompt": "exact generation prompt",
  "target_path": "absolute output path",
  "status": "pending",
  "receipt_path": "absolute receipt path"
}
```

Projects may use `combo_job_id` and `outfit_master_id`; the bundled planner recognizes both.

Reject duplicate IDs, duplicate target paths, missing references, or records with no exact prompt. A dispatch plan is derived data and must not replace the authoritative queue.
