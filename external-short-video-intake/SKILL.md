---
name: external-short-video-intake
description: Handle external short-video materials such as Douyin, TikTok China, Bilibili mirrors, creator batches, liked lists, collections, downloaded videos, transcripts, screenshots, keyframes, comments, and routing summaries. Use when the user provides short-video links, asks to download only, transcribe, analyze lightly, collect comments, fix gallery grouping, or prepare video materials for later project threads.
---

# External Short Video Intake

## Role

Handle short-video and creator-batch materials as external assets. Preserve source context, decide processing depth, and prepare both user-facing and thread-facing outputs.

## Core Rules

- Use existing local downloader workflows when available.
- Keep new materials in the external download zone or the user-specified external directory.
- Do not move, delete, rename, or internalize raw files by default.
- Do not analyze口播/tutorial videos formally before transcript or reliable captions exist.
- Use screenshots/keyframes for subtitle, lyric, UI, visual-workflow, and image-heavy materials.
- Treat comments as optional evidence. If comments matter but cannot be downloaded, report the gap.

## Batch Grouping

- Same-author account batch: group under the account.
- Favorites/liked list: group as the liked-list batch.
- Collection/playlist: group as the collection.
- Unrelated pasted links: keep separate, even if provided in one message.
- "Recent N" account downloads: use account-level grouping with per-item children.

## Routing Output

For each item or batch, record:

- source type
- author/account when known
- title or user-provided description
- local raw path
- transcript path/status
- screenshots/keyframes path/status
- comments path/status
- human gallery status
- thread index status
- suggested next action

