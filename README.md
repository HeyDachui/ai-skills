````markdown
# AI Handoff Consistency Skill

A reusable AI collaboration skill for keeping project goals, context, constraints, and execution boundaries aligned across AI conversations.

This Skill helps reduce goal drift, context loss, over-expansion, and inconsistent handoffs when working with AI across multiple conversations, tools, or project stages.

## What This Skill Solves

Long-running AI collaboration often breaks down when:

- A new AI conversation loses the original project context
- The AI expands the task beyond the intended scope
- The AI treats tools as the goal instead of serving the project goal
- Previously confirmed constraints are ignored or rewritten
- Handoff information is incomplete
- Different AI threads interpret the same project differently
- Analysis replaces real execution

This Skill is designed to make AI pause, verify, and align before continuing work.

## Use Cases

This Skill is useful when you need to:

- Move a project from one AI conversation to another
- Transfer work between ChatGPT, Codex, Claude, DeepSeek, or other AI tools
- Coordinate multiple AI threads on the same project
- Preserve project goals and constraints over time
- Prevent AI from automatically expanding the project scope
- Maintain consistency during long-term AI-assisted work
- Create cleaner handoff documents between AI sessions

## Not Intended For

This Skill is not meant for:

- Simple one-off questions
- Temporary tasks with no need for context continuity
- Generic prompt collections
- Replacing user judgment or project decisions
- Letting AI redesign the entire project direction
- Building an autonomous AI system or platform

## Core Principles

- Align before executing
- Confirm the project goal before taking action
- Preserve previously confirmed decisions
- Respect current task boundaries
- Do not expand scope without permission
- Do not replace production with analysis
- Do not treat tools as the purpose
- If a new instruction conflicts with confirmed context, warn first and ask for confirmation

## File Structure

```text
ai-handoff-consistency-skill-en/
├── SKILL.md      # Main Skill file
├── README.md     # Usage guide
````

If this repository contains both Chinese and English versions, the structure may look like this:

```text
ai-handoff-consistency-skill-zh/
├── SKILL.md
├── README.md

ai-handoff-consistency-skill-en/
├── SKILL.md
├── README.md
```

## How to Use

1. Open the `SKILL.md` file.
2. Copy the content into a new AI conversation, project instruction, or Skill-compatible environment.
3. Before asking the AI to execute a task, ask it to confirm:

   * Project goal
   * Current progress
   * Active constraints
   * Forbidden actions
   * Current task boundary
   * Next smallest executable step
4. Continue only after the AI has aligned with the confirmed context.

## Recommended Startup Prompt

You can use the following prompt when starting a new AI conversation:

```text
Please read and follow this Skill before executing any task.

Do not start implementation immediately.

First confirm the project goal, current progress, active constraints, forbidden actions, current task boundary, and the next smallest executable step.

If my new instruction conflicts with previously confirmed context, warn me first and ask for confirmation before proceeding.
```

## Typical Workflow

```text
1. Provide the Skill
2. Provide the project handoff summary
3. Ask the AI to restate the current goal and boundary
4. Check whether the AI has misunderstood or expanded the task
5. Correct the AI if needed
6. Confirm the next smallest executable step
7. Start execution
```

## Example Handoff Checklist

Before execution, the AI should be able to answer:

```text
Project goal:
Current stage:
Completed work:
Current task:
Allowed actions:
Forbidden actions:
Files or areas involved:
Next smallest executable step:
Possible conflict or ambiguity:
```

## Why This Matters

AI tools are powerful, but they often continue by guessing.
In long-term work, guessing can quietly rewrite the project.

This Skill creates a small but strict handoff gate: before the AI acts, it must first understand what should stay stable.

## Version Notes

This version is intended for public sharing and practical AI collaboration testing.

It may be updated based on real project use, especially in workflows involving multi-thread AI collaboration, project handoffs, and AI-assisted development.

## License

No license has been specified yet.

Before reusing, modifying, or redistributing this Skill, please check the repository license status.

```
```
