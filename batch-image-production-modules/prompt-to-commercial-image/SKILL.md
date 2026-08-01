---
name: prompt-to-commercial-image
description: "Turn one complex image request and its available references into a staged, reviewable production workflow: preserve the original input, extract a scene specification, generate and check a composition blockout, then add color, materials, lighting, and final detail without reopening approved structure. Use for advertising key visuals, character or product hero images, and complex illustrations where direct-to-final generation tends to drift in composition, proportion, hierarchy, or material. Do not use for batch queues, multi-image consistency systems, simple edits, or lightweight one-pass generation."
---

# Prompt to Commercial Image

Handle one target image at a time. Separate structure from finish so each failure returns to the stage that caused it instead of accumulating prompt patches.

## 1. Preserve the received input

- Save the request, prompt text, and reference files exactly as received. Do not overwrite them with a rewrite.
- State what each reference is allowed to control: subject, composition, pose, style, material, or negative example.
- Record source or rights status as `unknown` when it has not been checked.
- Label derived artifacts explicitly, for example `scene_spec`, `blockout_prompt_v1`, and `final_prompt_v1`.
- Never present a reconstructed, inferred, or reverse-engineered prompt as the historical prompt actually used.
- If the request says to preserve an attribute but the controlling reference or prior asset is missing, mark that attribute as blocked. Do not invent what must be preserved.

## 2. Extract a scene specification

Create a checkable specification that covers:

- purpose, aspect ratio, framing, and output requirements;
- subject identity, count, action, and invariants;
- camera, composition, position, scale, crop, occlusion, and depth layers;
- focal point, visual hierarchy, motion direction, negative space, and text-safe area;
- final color, material, lighting, atmosphere, and detail requirements;
- fixed, variable, forbidden, and still-unknown decisions.
- observable acceptance criteria or tolerances for the attributes that matter.

Distinguish received requirements, facts visible in references, production judgments, and unknowns. Resolve conflicts that would change the image meaning before making the blockout.

## 3. Generate and check the composition blockout

Generate a low-detail, grayscale, or neutral-material blockout that solves spatial structure before finish. A blockout is a structural checkpoint, not one mandatory visual style. Save the prompt actually sent, the generation entry, and the actual output.

Check:

- subject count, identity, action, and pose;
- camera, crop, perspective, position, and scale;
- silhouette, center of gravity, focal point, and negative space;
- foreground, middle ground, background, and occlusion;
- real room for required text, marks, or key objects.

Only pass the gate after viewing the output and recording the result. Use `blockout_checked_pass` for an internal check. Use `blockout_approved` only when a named approver explicitly approves it.

If the specification is wrong, return to the specification. If the specification is right but generation drifts, revise only the blockout prompt and regenerate. Do not proceed while structure fails.

## 4. Continue to color, materials, and final image

Use the checked blockout as the structural constraint and carry forward the original references that control identity, color, material, lighting, or style. Add color, materials, lighting, atmosphere, and final detail while preserving the accepted camera, subject position, scale, pose, silhouette, depth, and visual weight. If the generation entry cannot accept both structural and appearance references, record the limitation and chosen workaround instead of silently dropping either constraint.

A separate color-or-material intermediate is optional, not mandatory. Add that checkpoint only when color relations are complex, material meaning is ambiguous, the generation entry requires it, or a direct final pass drifts at that layer.

Save the prompt actually sent, the generation entry, and the actual output. Do not treat a simulated interface, editorial illustration, or operation that never occurred as generation evidence.

## 5. Review and return to the responsible stage

Compare the final image with the preserved input, scene specification, and checked blockout. Record each item as `pass`, `fail`, or `unknown`:

- requested meaning and subject;
- composition, scale, pose, and spatial hierarchy;
- color, material, lighting, and visual hierarchy;
- defects, edges, details, and file requirements;
- asset, font, portrait, brand, and model rights when commercial use is intended.

Route failures:

- misunderstood or conflicting intent → scene specification;
- camera, composition, position, scale, pose, or depth → blockout;
- color, material, lighting, texture, or finish → final stage;
- cause cannot be located → keep `unknown` and obtain evidence before choosing.

Keep each retry and its failure reason. Do not overwrite the received input, checked blockout, or earlier output. Set retry limits from task cost and observed progress, not an arbitrary fixed count.

## Minimum evidence

Keep:

1. the received request and reference record;
2. the scene specification;
3. the actual blockout prompt, output, and gate result;
4. the actual final prompt, output, and review result;
5. the tool, model, or entry actually used plus any available job ID, parameters, or timestamps.

This evidence proves only the recorded run and checks. One success does not prove stable reproduction. Do not claim commercial readiness before rights and delivery conditions are checked, and do not claim an image was generated without a real run record.

