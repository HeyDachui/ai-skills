---
name: external-note-platform-intake
description: "Collect and organize Xiaohongshu-style note platform materials: profiles, notes, images,正文, visible comments, likes, collects, comment counts, search samples, and semi-automatic logged-in browser collection. Use when the user provides Xiaohongshu profiles, note links, topic keywords, or asks for a visual and structured note archive without manual screenshot copying."
---

# External Note Platform Intake

## Role

Collect note-platform materials in a low-frequency, read-only, semi-automatic workflow. Optimize for useful text, images, engagement metrics, visible comments, and source traceability.

## Safety

- Do not read, export, or save cookies, tokens, session IDs, or sensitive URL parameters.
- Do not like, favorite, follow, comment, publish, or message.
- Logged-in browsing is allowed only when the user has opened or approved the logged-in context.
- If automation becomes unstable, fall back to user-opened page extraction or manual copy-assisted collection.

## Collection Priority

1. Profile/index-level listing.
2. Single-note detail page extraction.
3. Visible comments and engagement metrics.
4. Image/cover collection or references.
5. Human visual entrance.
6. Thread structured entrance.

## Output Shape

For each note, preserve:

- author
- title
-正文
- images/covers when available
- likes, collects, comments, and visible comment excerpts
- source page description with sensitive parameters removed
- collection time
- confidence and missing fields

Do not deliver raw JSON as the only user-facing result.
