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
