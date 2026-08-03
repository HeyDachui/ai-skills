# prompt-to-commercial-image

中文名：**提示词到商业成图**

Turn one complex image request into a staged, reviewable workflow: preserve the received input, extract a scene specification, check a composition blockout, and then add color, materials, lighting, and final detail without reopening approved structure.

适用于广告主视觉、角色或产品英雄图、复杂插画等单张复杂成图任务。它解决的是“直接生成终稿时，构图、比例、层级或材质不断漂移”的问题，不是批量出图队列，也不会代替真实生成工具。

## Open the Skill

- Skill instructions: [SKILL.md](SKILL.md)
- Codex agent metadata: [agents/openai.yaml](agents/openai.yaml)
- Public source: <https://github.com/HeyDachui/ai-skills/tree/main/batch-image-production-modules/prompt-to-commercial-image>

## Install

Clone or download the public repository, then copy this directory into the Skills directory used by your AI client:

```text
batch-image-production-modules/prompt-to-commercial-image/
```

For Codex, a typical destination is:

```text
~/.codex/skills/prompt-to-commercial-image/
```

Restart or reload the client if it does not discover newly added Skills automatically.

## Use

Invoke the Skill by name and provide the image request plus any references:

```text
Use $prompt-to-commercial-image to turn this complex image request into a staged, reviewable production workflow.
```

The workflow keeps structural approval separate from finish work. It does not claim that an image was generated unless there is a real run record, and it does not claim commercial readiness before asset, portrait, brand, model, and delivery conditions are checked.

## Public Sharing Boundary

This directory is part of the public `batch-image-production-modules` package. See the parent [README](../README.md) and [NOTICE](../NOTICE.md) for the current attribution and sharing terms. This folder does not add a separate license.
