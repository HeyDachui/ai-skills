---
name: finalize-image-production
description: "Finalize a batch image-production delivery by reconciling queue records, local images, receipts, terminal blocks, exclusions, prompts, machine indexes, and a human-readable report. Use when production is ending or when completion claims conflict with local evidence."
---

# Finalize Image Production

Run:

`python scripts/finalize_delivery.py --queue <queue.json> --reports-dir <reports> --output-dir <delivery>`

The finalizer produces:

- machine-readable item index;
- JSONL prompt archive with technical fields;
- plain-text full prompt edition without technical fields;
- completion and exception report;
- audit summary.

Completion means every item is reconciled as a valid image, terminal block, intentional exclusion, or explicitly unresolved item. Preserve unresolved counts and do not rewrite them as success.

Before claiming production-ready, open the generated artifacts, validate UTF-8, count records, and follow at least one real consumer path.

See [references/finalization-contract.md](references/finalization-contract.md).
