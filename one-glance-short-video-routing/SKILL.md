---
name: one-glance-short-video-routing
description: "Use when handling external short-video materials such as Douyin/TikTok China links, downloaded videos, transcripts, screenshots, image posts, creator batches, or visual gallery items. The skill downloads and transcribes when needed, checks duplicates, separates primary media from auxiliary files, identifies the user's likely reference intent, and routes each material as skip, retain, light analysis, deep analysis, handoff, or external candidate asset. Trigger when the user asks to download, transcribe, analyze, classify, tag, route, hand off, or decide how to use short-video materials."
---

# 一眼分流法：短视频下载转写与意图分流 Skill

版本：v1.0.0

## 定位

Use this skill as the first handling layer for external short-video materials entering a local workspace.

Do not treat it as a normal summary skill. Its core job is to decide why the user saved the material before deciding how deeply to process it.

## Core Principles

1. Treat downloading as material acquisition, not analysis completion.
2. Treat analysis as external-material interpretation, not internal asset adoption.
3. Keep external materials external by default.
4. Identify reference intent before choosing analysis depth.
5. Separate primary media, transcripts, raw downloads, screenshots, keyframes, reports, and auxiliary files.
6. Mark uncertain intent as `pending_intent` instead of forcing a workflow translation.
7. Proactively flag high-value materials, but do not write them into internal rules, formal skills, prompt panels, or formal knowledge bases without review.

## Reference Intent Tags

Assign one or more tags to every material:

| Tag | Use When |
|---|---|
| `content_reference` | The user likely wants the knowledge, argument, method, or tutorial. |
| `presentation_reference` | The user likely wants the title, opening, narration, structure, pacing, or editing pattern. |
| `visual_style_reference` | The user likely wants composition, color, character, atmosphere, motion, or aesthetic style. |
| `prompt_or_generation_reference` | The user likely wants prompt wording, camera terms, material terms, motion terms, or generation method. |
| `workflow_reference` | The user likely wants the toolchain, operation steps, stages, checks, or acceptance criteria. |
| `account_strategy_reference` | The user likely wants account positioning, topic selection, repeatable formats, or growth pattern. |
| `audio_rhythm_reference` | The user likely wants music, pauses, sound design, voice rhythm, or audio-visual timing. |
| `retention_only` | The user only wants to save the material for now. |
| `pending_intent` | The user's reason for saving the material is unclear. |

Reference intent is multi-label, not a single-choice field.

## Standard Workflow

1. Identify the source type.
   - Single video, profile batch, image post, screenshot, article, existing local folder, report-only source, or old material review.

2. Check duplicates.
   - Search local indexes, source directories, gallery data, reports, and prior manifests.
   - Prefer display-layer dedupe. Do not physically delete duplicate files by default.

3. Download and transcribe when needed.
   - For spoken videos or tutorial videos, obtain transcripts whenever feasible.
   - Use the project-approved local downloader/transcriber first when one exists.
   - Set UTF-8 environment safeguards before commands that read or write Chinese text, Markdown, JSON, transcripts, reports, or indexes.

4. Separate material layers.
   - Keep primary videos/images separate from raw downloads, transcripts, keyframes, contact sheets, screenshots, reports, and generated indexes.
   - Do not mix auxiliary files into the user's main browsing surface unless they are explicitly useful as previews.

5. Infer user reference intent.
   - Use the user's wording, current project context, title, source type, visible format, transcript, and previous handling patterns.
   - When uncertain, write `pending_intent` and explain the risk.

6. Route the material.
   - Choose one or more routes:
     - `skip`
     - `retain`
     - `light_analysis`
     - `deep_analysis`
     - `handoff`
     - `external_candidate_asset`
     - `needs_visual`
     - `needs_transcript`
     - `needs_user_confirmation`

7. Write a bounded report or handoff.
   - Keep the report aligned with the chosen intent.
   - Do not use a workflow template when the material is only visual reference.
   - Do not force entertainment, aesthetic, or mood materials into procedural workflow form.

## Analysis Contract

When analyzing, explicitly separate:

- `material_explicitly_says`
- `inferred_from_material`
- `local_adaptation`
- `needs_user_confirmation`

Use concise outputs for low-value materials. Use deeper structures only for materials that can clearly improve a reusable workflow, rule, prompt, skill, review gate, or handoff pattern.

## Suggested Output Depth

### Lightweight Material

```text
WORKFLOW_CARD
ACCEPTANCE_CARD
```

### Medium-Value Material

```text
WORKFLOW_CARD
STAGE_CONTRACTS
ACCEPTANCE_CARD
```

### High-Value Material

```text
WORKFLOW_CARD
STAGE_CONTRACTS
SUBFLOW_LIBRARY
ACCEPTANCE_CARD
HANDOFF_STATE_PACK
SKILL_DRAFT
PROMPTCOPY_ENTRY
```

Do not generate the full high-value structure by default. Use it only when the material clearly contributes to the local system.

## Skip And Defer Rules

Mark a material as `skip` or `pending_intent` when:

- The user explicitly says not to analyze it.
- The material is a clearly marked AI image account and the user only wants retention or browsing.
- The material is image-based but the current task asks to skip images.
- The transcript is unusable and no visual analysis is requested.
- The material has no visible reusable value for the current project.
- The likely reference intent conflicts with the user's latest instruction.

## High-Value Signals

Proactively flag material when it can:

- Improve a reusable workflow, skill, prompt, or rule.
- Explain a recurring project problem.
- Reduce rework or handoff friction.
- Provide a new acceptance standard or review gate.
- Become a structured external candidate asset after local adaptation.

Flagging high value is not internalization. Internalization requires local adaptation, boundary review, and user approval.

## Safety And Boundaries

Do not:

- Absorb external material directly into internal formal assets.
- Modify global rules or formal knowledge bases.
- Modify prompt panels or active instruction surfaces.
- Delete, move, or rename original materials by default.
- Read, print, copy, or store cookies, tokens, passwords, or API keys.
- Continue analysis from visibly corrupted or garbled text.
- Treat an unconfirmed reference intent as fact.

## Completion Report

End with a short checkable report:

```text
完成情况：
1. 下载/转写了哪些内容：
2. 跳过了哪些内容及原因：
3. 参考意图判断：
4. 输出位置：
5. 是否发现高价值内容：
6. 是否需要用户确认：
7. 编码处理：
```
