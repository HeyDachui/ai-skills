# Routing Reference

## Material Types

- `main`: primary downloaded video, image set, audio, webpage, or conversation.
- `raw`: raw downloader or scraper output.
- `txt`: transcript, OCR text, copied text, or extracted page text.
- `keyframes`: representative frames from video.
- `screenshots`: screenshots used for visual inspection, lyric calibration, UI evidence, or OCR.
- `comments`: visible comments, replies, or engagement-led discussion.
- `reports`: routing summaries, analysis reports, manifests, and handoff notes.
- `gallery`: human-facing visual entrance.
- `thread_index`: structured entrance for later threads.

## One-Glance Routing Questions

Ask:

1. Why did the user likely save this?
2. Is it a tutorial, inspiration, evidence, account sample, music reference, game guide, UI/visual case, platform tactic, or comment clue?
3. Does serious analysis require transcript, OCR, screenshots, comments, audio features, or original source comparison?
4. Is it a single item, same-author batch, favorites list, collection, or unrelated bundle?
5. Which later project thread is likely to use it?

## Processing Decisions

- **Download only**: Use when the user explicitly says only download or when the material is a low-risk raw reference.
- **Transcribe**: Use for speech, explanation, tutorial, commentary, or口播 videos before formal analysis.
- **OCR/screenshots**: Use for image posts, subtitles, lyrics, UI tutorials, visual workflows, or cases where transcript is missing/inaccurate.
- **Comments**: Use when comments contain correction, usage method, social proof, platform response, or adoption signals.
- **Audio/music analysis**: Use when music itself matters, not only lyrics. Preserve audio source and distinguish original, cover, remix, platform generation, and user prompt.
- **Light report only**: Use when material is clearly low value or when project threads will perform domain analysis later.

## Display Grouping

- Group same-author bulk downloads under the creator/account batch.
- Group favorites/liked-list batches as favorites list, not as unrelated standalone items.
- Group collections/playlists as collections.
- Do not group unrelated single links merely because the user pasted them together.
- For "recent N" account downloads, keep account-level grouping and expose per-item children inside the group.
- Allow multi-tags when one material belongs to several uses.

## Status Labels

Use compact status labels:

- `downloaded`
- `metadata_only`
- `needs_transcript`
- `transcribed`
- `needs_ocr`
- `needs_comment_check`
- `needs_visual_review`
- `light_analyzed`
- `handoff_ready`
- `blocked`
- `external_reference_only`

