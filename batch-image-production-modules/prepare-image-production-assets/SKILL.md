---
name: prepare-image-production-assets
description: "Validate reference images, action assets, outfit assets, recipes, prompts, and target paths before batch image generation. Use when source materials must be deduplicated, classified as ready or blocked, and converted into a production-ready manifest without inventing missing visual evidence."
---

# Prepare Image Production Assets

Establish what can actually be produced before building or dispatching a queue.

Run:

`python scripts/audit_assets.py --queue <queue.json> --output <asset-audit.json>`

Check:

- every job has a unique ID and target;
- every required reference exists and is a file;
- every job contains an exact final prompt;
- group and variation identities are present when diversity control depends on them;
- duplicated references are intentional rather than accidental;
- incomplete evidence is blocked instead of being completed by guesswork.

Output ready and blocked records with reasons. Do not generate images, mutate the queue, or claim visual quality.

See [references/asset-readiness.md](references/asset-readiness.md).
