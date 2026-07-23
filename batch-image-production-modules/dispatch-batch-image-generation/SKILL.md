---
name: dispatch-batch-image-generation
description: "Create explicit worker packets for batch image generation while isolating image/Base64 responses from the controller. Use when multiple jobs or workers must receive exact IDs, prompts, references, output paths, receipt requirements, retry limits, and a prohibition on autonomous continuation."
---

# Dispatch Batch Image Generation

Create worker packets from an authoritative queue and an approved dispatch plan:

`python scripts/make_dispatch_packets.py --queue <queue.json> --plan <plan.json> --output-dir <packets> --workers 3`

Each packet must contain only explicit jobs and their exact:

- job ID;
- reference path;
- final prompt;
- target path;
- receipt path;
- retry policy.

Workers must save images and receipts locally, avoid returning Base64 to the controller, and stop after the listed jobs. They must not self-select or continue automatically.

Before dispatch, skip any job whose valid target already exists. After dispatch, let the receipt-control workflow reconcile facts.

See [references/worker-contract.md](references/worker-contract.md).
