---
name: compose-reference-image-prompts
description: "Compose and validate reference-guided image prompts that separate fixed visual dimensions from variable dimensions and acceptance criteria. Use when prompts must preserve an outfit, product, pose, or other reference evidence without copying irrelevant identity, scene, or unsupported details."
---

# Compose Reference Image Prompts

Build each prompt from four explicit parts:

1. reference role and what it is allowed to fix;
2. fixed dimensions that must remain faithful;
3. variable dimensions that may change;
4. composition, safety, and acceptance requirements.

Validate a queue of final prompts:

`python scripts/validate_prompts.py --queue <queue.json> --required-phrase <phrase>`

Use project-specific required phrases only as parameters. Do not embed client names, asset IDs, private paths, or one project’s exclusions into the Skill.

Do not infer garments, objects, relationships, or actions that the reference does not support. Preserve the exact prompt actually sent in the receipt.

See [references/prompt-contract.md](references/prompt-contract.md).
