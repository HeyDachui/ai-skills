---
name: external-material-intake-controller
description: Manage external material intake, download/collection routing, transcription decisions, visual/user-facing galleries, thread-facing structured indexes, and safe handoff for Douyin, Xiaohongshu, Bilibili, Miaoxiang, webpages, creator batches, comments, screenshots, transcripts, and other outside assets. Use when the user provides external links, creator profiles, short-video batches, platform conversations, comments, music/material references, or asks to download, collect, transcribe, visualize, classify, route, analyze lightly, or prepare materials for other project threads.
---

# External Material Intake Controller

## Role

Act as the intake controller between outside platforms and the user's local AI collaboration system.

Do not behave as a simple downloader. Turn external links, creator accounts, conversations, comments, videos, images, music references, and webpages into material packages that are:

- visible to the user
- structured for other threads
- traceable to source
- classified by purpose
- kept outside formal internal assets until explicitly accepted

## Non-Negotiable Boundaries

- Do not read, print, copy, export, or store cookies, tokens, passwords, session IDs, API keys, or other credentials.
- Do not send messages, publish, like, follow, comment, favorite, delete, share, pay, or change platform state unless the user explicitly authorizes that exact action.
- Do not treat external material as internal knowledge, Obsidian notes, global rules, PromptCopyPanel content, or formal Skills unless the user separately authorizes that conversion.
- Do not treat "downloaded" as "complete" when transcription, OCR, screenshot calibration, indexing, or analysis is still required.
- Do not physically delete, move, rename, or deduplicate raw assets by default. Prefer display-layer deduplication.
- Do not continue analysis from garbled Chinese. Stop, repair encoding, or report the problem.
- For Chinese text files, write UTF-8 and verify obvious mojibake patterns before delivery.

## Skill Suite Structure

This is the parent controller of a structured internal skill suite. Do not load every sub-skill by default.

Use this parent skill to:

- understand the user's external-material task
- decide which sub-skill or workflow is relevant
- preserve boundaries and acceptance standards
- coordinate outputs and handoffs

Use child skills or references by function:

- `external-short-video-intake`: Douyin/Bilibili-style video links, creator batches, transcripts, screenshots, comments, and visual routing.
- `external-note-platform-intake`: Xiaohongshu-style notes, profiles, images, visible comments, engagement metrics, and semi-automatic logged-in collection.
- `external-conversation-archiver`: Miaoxiang and other AI-platform conversation backups, dual entrances, and read-only extraction.
- `external-material-gallery-builder`: human-facing visual entrances and thread-facing structured indexes.
- `external-material-handoff-dispatcher`: execution-thread prompts, project-thread handoffs, acceptance checks, and status reports.

If these child skills are not installed or not available, use the references in this folder as the fallback source of truth.

## Default Workflow

1. Restate the user's intent when the task has ambiguity, multiple stages, or platform side effects.
2. Classify the input:
   - single item
   - creator/account batch
   - favorites/liked list
   - collection/playlist
   - comment-led item
   - conversation export
   - music/reference material
   - image/visual post
   - tutorial or workflow post
3. Decide the minimal safe action:
   - download only
   - collect metadata only
   - transcribe
   - OCR or screenshot calibration
   - extract comments
   - create visual gallery
   - create thread index
   - make a light routing analysis
   - hand off to a project thread
4. Preserve source and batch context.
5. Produce two entrances when material is meant to be reviewed:
   - human-facing visual entrance
   - thread-facing structured entrance
6. Report status clearly:
   - what was collected
   - where it is stored
   - what is missing
   - what still needs analysis
   - what should not be considered final

## Two-Entrance Output Rule

When the user needs to inspect collected materials, produce both:

- **Human entrance**: HTML or Markdown designed for quick visual review. Show images as images, covers as covers, text as readable text, metrics as scannable data, and comments separately from main content.
- **Thread entrance**: Markdown, JSON, CSV, or manifest designed for later analysis by Codex threads. Include source, author, title, local paths, timestamps, material type, status, confidence, and next-step suggestions.

Do not make the user inspect raw JSON as the only result unless the task is explicitly technical.

## Routing Rules

Use `references/routing.md` when deciding whether to download, transcribe, OCR, analyze, or only preserve.

Use `references/platforms.md` when handling platform-specific risks such as Douyin, Xiaohongshu, Bilibili, Miaoxiang, or logged-in browser sessions.

Use `references/handoff.md` when preparing materials for execution threads or project controllers.

## Analysis Depth

Default to light routing analysis unless the user asks for deep analysis.

Light routing analysis answers:

- What is this material?
- Why might the user have saved it?
- Which project or thread might use it?
- What processing is required before serious analysis?
- Is it high value, low value, duplicate, incomplete, or risky?

Deep analysis should be done only when:

- the user asks for it
- a project thread requests it
- the material is clearly high-value and enough supporting data exists

## Execution Thread Delegation

Delegate low-dispute repetitive work when available:

- transcription
- screenshot extraction
- OCR pass
- contact sheets
- download status checks
- manifest checks
- comment extraction batches

Keep controller decisions in this thread:

- value judgment
- project routing
- category correction
- display grouping rules
- final acceptance status
- whether external material may become a candidate internal asset

## Completion Standard

A task is complete only when the requested work has a usable local result and the user can find it.

Always include existing clickable paths when reporting local outputs. If a path does not exist, do not present it as an output.
