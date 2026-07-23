# Batch Image Production Modules

Eight small, independent Skills for a complete, evidence-based batch image-production workflow. Use one module when that is all you need, or combine them in this order:

`asset preparation → prompt composition → queue building → dispatch → receipt control → quality curation → review gallery → finalization`

## Modules

1. `prepare-image-production-assets` — verify references, prompts, job IDs, and target paths before production.
2. `compose-reference-image-prompts` — make the fixed and variable dimensions of reference-guided prompts explicit.
3. `build-image-combination-queue` — build auditable, deduplicated queues and explicit batches.
4. `dispatch-batch-image-generation` — create bounded worker packets with exact jobs, paths, prompts, receipts, and retry rules.
5. `control-image-generation-receipts` — reconcile local images, receipts, hashes, prompts, retries, and blocks.
6. `curate-image-production-quality` — surface repetition and record reversible human keep/hide/reject decisions.
7. `build-image-review-gallery` — build a local UTF-8 HTML gallery with grouping and broken-image indicators.
8. `finalize-image-production` — reconcile delivery evidence and generate indexes, prompt archives, and exception reports.

## What is intentionally not included

This is the public modular edition. The integrated controller, real project queues, generated images, prompt collections, receipts, test outputs, local absolute paths, and operating evidence are not included.

## Requirements

- Python 3.9+; standard library only.
- Local JSON queue records and local file paths supplied by the user or project.
- Human review for visual quality, safety, ownership, and final publication decisions.

## Public sharing and AI-use notice

These modules are shared for learning, noncommercial practice, and responsible reuse. You may study, run, and forward them with source attribution. Please retain the source link and do not present the work as your own.

Do not use them for unlawful activity, infringement, evading platform safeguards, or mass production of content you do not have the right to create or distribute. This package is a workflow aid, not legal advice, a rights clearance, or a guarantee that generated content is safe or compliant.

For commercial use or redistribution without attribution, contact the maintainer first.

Source: <https://github.com/HeyDachui/ai-skills/tree/main/batch-image-production-modules>

See [NOTICE.md](NOTICE.md) and [ASSET_MANIFEST.json](ASSET_MANIFEST.json) for the package boundary and provenance record.
