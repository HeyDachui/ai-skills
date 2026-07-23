---
name: build-image-review-gallery
description: "Build local UTF-8 HTML galleries for reviewing batch-generated images with grouping, numbering, prompt lookup, default exclusions, and image-load checks. Use when reviewers need a complete or batch view while controlling repeated outfits and retaining hidden historical outputs."
---

# Build Image Review Gallery

Generate the review page from queue records and real local images:

`python scripts/build_gallery.py --queue <queue.json> --output <review.html> --max-per-group 3`

Requirements:

- include only files that exist;
- use paths that resolve from the HTML location;
- write UTF-8 with an explicit charset;
- show stable review numbers and useful human labels;
- group or order images to avoid long runs of one outfit/group;
- preserve intentionally hidden history without showing it by default;
- include an image-load failure indicator in the page.

Do not let gallery ordering rewrite queue identity. A review number is presentation metadata, not a job ID.

See [references/gallery-acceptance.md](references/gallery-acceptance.md).
