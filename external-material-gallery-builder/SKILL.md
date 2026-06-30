---
name: external-material-gallery-builder
description: Build human-facing visual entrances and thread-facing structured indexes for collected external materials, including videos, images, notes, comments, transcripts, screenshots, creator batches, liked lists, and conversation archives. Use when the user wants to visually inspect collected material or when other threads need a structured manifest.
---

# External Material Gallery Builder

## Role

Turn collected external material into two entrances:

- a human-facing visual entrance
- a thread-facing structured entrance

## Human Entrance

Make the user able to inspect material quickly:

- show images as images
- show covers or thumbnails when useful
- show正文 as readable text
- show comments separately from main content
- show metrics compactly
- group same-author account batches
- avoid hiding everything behind filenames

The interface may be plain, but it must be usable and quick to scan.

## Thread Entrance

Make other threads able to continue work:

- JSON, CSV, Markdown manifest, or all three
- stable local paths
- source description
- author/account
- batch/group id
- material type
- status labels
- processing gaps
- suggested next action

## Grouping

- Same-author bulk account downloads: one group with children.
- Liked/favorites list: one group with children.
- Collection/playlist: one group with children.
- Unrelated one-off links: separate groups.
- Allow multi-tags when one item belongs to several project uses.

