---
name: control-image-generation-receipts
description: "Reconcile batch image-generation results against local files, receipts, hashes, prompts, and queue records. Use when worker completion claims, missing images, duplicate generation, network retries, moderation blocks, or stale queue statuses must be resolved without loading image/Base64 responses."
---

# Control Image Generation Receipts

Use local evidence to determine production state.

Run:

`python scripts/audit_production.py --queue <queue.json> --reports-dir <reports> --output <audit.json>`

For every job, compare:

- queue job ID and receipt job ID;
- queue target and receipt target;
- actual local file existence and size;
- receipt byte count and SHA-256 when present;
- queue prompt and receipt final prompt;
- generation status, retry permission, and visual-review status.

Rules:

- Existing valid image: never regenerate solely because queue status is stale.
- Receipt without image: unresolved, not complete.
- Image without receipt: preserve image and request/reconstruct evidence; do not call it accepted.
- Non-retryable moderation block: preserve evidence and exclude from dispatch.
- Network failure: retry only within the project’s stated retry policy.
- Visual drift: mark for human review; do not automatically consume another generation.

See [references/receipt-policy.md](references/receipt-policy.md).
