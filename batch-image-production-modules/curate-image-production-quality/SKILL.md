---
name: curate-image-production-quality
description: "Analyze visual-group concentration and record reversible human selection decisions for generated image collections. Use when repeated outfits, weak variants, rejected images, or default-hidden history must be controlled without deleting source files or confusing presentation choices with production facts."
---

# Curate Image Production Quality

Use local images and queue metadata to expose repetition:

`python scripts/analyze_diversity.py --queue <queue.json> --output <diversity.json> --preferred-visible-per-group 5`

The script reports concentration and review candidates; it does not make aesthetic decisions.

Human reviewers decide:

- which images are strong enough to keep visible;
- whether images truly show the same outfit or only share a metadata group;
- which actions are redundant;
- whether anatomy, reference fidelity, or composition requires rejection.

Record decisions as `visible`, `hidden`, `rejected`, or `needs_review`. Keep source files unless deletion is explicitly authorized. A hidden image remains production history.

See [references/curation-policy.md](references/curation-policy.md).
