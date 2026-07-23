# Receipt policy

A useful receipt records the job identity, actual prompt, reference paths, target path, bytes, SHA-256, generation count, retry count, completion time, generation status, retry permission, and visual-review conclusion.

Older receipts may omit some fields. Report missing evidence rather than fabricating it.

Terminal moderation detection requires both:

```text
generation_status = moderation_blocked
retry_allowed = false
```

If a provider does not supply retry permission, keep the state unresolved until the project policy decides it.
