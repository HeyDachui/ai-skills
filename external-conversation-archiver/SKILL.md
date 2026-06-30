---
name: external-conversation-archiver
description: Archive external AI-platform conversations such as Miaoxiang, music studio agent sessions, browser-based chat tools, and other logged-in web conversations. Use when the user wants to save, restore, visualize, structure, or hand off a long platform conversation while preserving read-only safety and avoiding credential capture.
---

# External Conversation Archiver

## Role

Back up long external platform conversations into local files that the user can read and other threads can analyze.

## Safety

- Use only read-only extraction unless the user explicitly authorizes sending a specific prompt.
- Do not blindly type into a page if browser control is unstable.
- Do not save cookies, tokens, session IDs, full sensitive URLs, passwords, or account secrets.
- Redact sensitive URL parameters in reports and structured files.

## Required Outputs

Save at least:

- `HUMAN_VIEW.html`: readable visual entrance for the user.
- `THREAD_VIEW.md`: structured conversation for threads.
- `THREAD_VIEW.json`: machine-readable message list.
- `RAW_TEXT_BACKUP.txt`: simple recovery backup.
- `COLLECTION_METHOD.md`: short explanation of how the collection was performed.

## Message Structure

When possible, split messages by:

- index
- role
- text
- character count
- source page title
- extraction time

If role detection is uncertain, mark it as `unknown` instead of guessing silently.

