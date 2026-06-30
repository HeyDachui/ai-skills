# Platform Reference

## Douyin

- Use the local downloader and existing download zone workflow when possible.
- New downloads default to the configured external download zone, not internal assets.
- For creator batches, preserve account-level grouping.
- For口播 or tutorial videos, do not perform formal analysis before transcript or reliable captions exist.
- For subtitle-heavy, lyric-heavy, UI-heavy, or visual workflow videos, use screenshots or keyframes to calibrate text.
- Comment download may be unavailable or unstable; if comments matter and cannot be collected, report that gap.

## Xiaohongshu

- Prefer low-frequency, read-only collection.
- Logged-in browser collection may expose正文, images, visible comments, likes, collects, and comment counts, but can trigger rate limits.
- Do not save sensitive URL parameters, cookies, tokens, or session material.
- For each collected note, produce:
  - readable content for the user
  - structured JSON/Markdown for threads
  - image/cover references when available
  - metrics and visible comments when relevant
- If full automation fails, fall back in order:
  1. profile/index-level collection
  2. logged-in single-note DOM extraction
  3. user-opened page collection
  4. manual copy-assisted collection

## Bilibili

- Check whether the task needs a single video, UP主 batch, playlist, or metadata only.
- If batch collection is fragile, evaluate whether the same creator exists on a more reliable platform before proceeding.
- Keep Bilibili source and Douyin mirror source distinct if both exist.

## Miaoxiang / Music Studio

- Treat conversations as external platform sessions.
- Read-only extraction from an already-open logged-in Chrome page is acceptable when the user requests backup.
- Save conversation backups as:
  - human-facing HTML
  - thread-facing Markdown/JSON
  - raw text backup
  - short collection method note
- Sending prompts to the platform is a side-effect. Require explicit authorization for the exact prompt or a clearly bounded batch.
- If browser control is unstable, do not blindly type into the active window. Ask the user to send manually or re-establish a safer control path.

## Webpages And Other Platforms

- Use read-only collection first.
- Save source URL, retrieval time, title, and visible text or media references.
- If precise or current public information is needed, verify from primary or official sources where possible.

