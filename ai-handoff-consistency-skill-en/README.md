# Dialogue Consistency Review Skill

## Purpose

This Skill helps a new ChatGPT conversation, a new Codex thread, or another AI tool instance take over an existing project.

It solves this problem:

A new conversation appears to understand the task, but its actual direction does not match the user's real intent.

## Core Rule

Do not enter production before passing the consistency review.

## Recommended Usage

Enter this in a new conversation:

Please start the "Dialogue Consistency Review Skill".

The current task is not to produce content directly and not to execute the project directly.

Your task is to first take over the existing project and prove whether you truly understand the project boundaries, current stage, real intent, and what must not be done.

Please first read the handoff materials I provide, judge whether the materials are sufficient, and identify possible drift risks.

If materials are insufficient, first use a structured interview to fill the gaps.

If materials are sufficient, generate the "New Conversation Consistency Review Package", and I will send it to the previous conversation for verification.

Highest rule: Do not enter production before passing the consistency review.

## Standard Process

Read handoff materials  
→ Material sufficiency judgment  
→ Risk identification  
→ Follow-up interview  
→ Generate consistency review package  
→ Previous-conversation verification  
→ Revise handoff rules  
→ User confirmation  
→ Minimal execution

## Applicable To

- New ChatGPT conversation
- New Codex thread
- AI workflow handoff
- Project handoff
- New conversation restart after a long conversation becomes slow or stuck
- Content production project
- Engineering project
- Obsidian workflow
- Game / worldbuilding project

## Not Applicable When

If the user is only asking a simple temporary question and no old-project handoff is involved, this Skill does not need to be started.
