# Batch Image Production Modules

Four small, independent Skills for reliable batch image-production work. They may be used alone or combined in this order:

`queue → receipts → review gallery → finalization`

## Modules

- `build-image-combination-queue` — turn source assets and exact prompts into a stable, deduplicated production queue and explicit batches.
- `control-image-generation-receipts` — reconcile local images, receipts, hashes, prompts, retries, and safety blocks before treating work as complete.
- `build-image-review-gallery` — build a local UTF-8 HTML review gallery with grouping and broken-image indicators.
- `finalize-image-production` — reconcile the queue and generate a machine index, prompt archive, audit summary, and human-readable report.

## What is intentionally not included

This is the public modular edition. The original integrated controller, project-specific tests, real queues, production prompts, generated images, and operational evidence are not included.

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
