# Asset readiness

Classify each record as:

- `ready`: all required local evidence and production fields exist;
- `blocked_missing_reference`: required reference is missing;
- `blocked_missing_prompt`: no exact final prompt;
- `blocked_ambiguous_identity`: stable job or target identity is missing or duplicated;
- `blocked_source_evidence`: a human or upstream process declared the evidence insufficient.

Blocking is not rejection. New evidence may make the record ready later.
