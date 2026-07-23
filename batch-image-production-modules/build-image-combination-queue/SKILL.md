---
name: build-image-combination-queue
description: "Build and validate auditable image-production queues from action, outfit, prompt, or other combinable source assets. Use when jobs need stable IDs, deduplication, explicit references, diversity-aware batches, exclusion rules, and deterministic target paths before generation begins."
---

# Build Image Combination Queue

Create the queue before generation. One record must represent one immutable production intent.

## Required record contract

Each record needs:

- unique job ID and stable order number;
- source/reference asset path;
- grouping key such as outfit ID;
- variation key such as action family;
- exact final prompt;
- deterministic target path;
- status and receipt path.

Validate that referenced inputs exist, job IDs and target paths are unique, and no record silently changes another record’s prompt or reference.

Use:

`python scripts/plan_batches.py --queue <queue.json> --reports-dir <reports> --output <plan.json> --batch-size 12 --max-per-group 3`

The planner must:

- skip terminal blocks and intentional exclusions;
- skip records whose target image already exists;
- favor different groups, then different variation families;
- output explicit job IDs rather than letting workers self-select.

Do not invent new recipes merely to make a batch look balanced. Report source-data limits instead.

See [references/queue-schema.md](references/queue-schema.md) for field aliases and validation rules.
