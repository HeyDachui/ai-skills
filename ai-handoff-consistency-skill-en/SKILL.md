---
name: Dialogue Consistency Review Skill
description: Used when a new ChatGPT conversation or Codex thread takes over an existing project. It first completes material assessment, follow-up interview, previous-conversation verification, and minimal-execution limits to prevent surface-level understanding from drifting away from the actual direction.
---

# Dialogue Consistency Review Skill

## 1. Skill Goal

This Skill is used to solve the following problem:

A new conversation appears to understand the task and outputs content in the expected format, but its actual direction does not match the user's real intent.

The goal of this Skill is not to make AI write better, nor to make AI enter production faster. Its goal is to ensure that when a new conversation takes over an existing project, it first completes:

- Understanding the project boundaries
- Understanding the user's real intent
- Understanding the current stage
- Understanding what must not be done
- Understanding how to accept correction
- Passing a verifiable consistency review

Core self-check sentence:

Do not enter production before passing the consistency review.

---

## 2. Applicable Scenarios

This Skill should be triggered when the user asks for any of the following:

- Take over this project
- Continue the previous project
- This is a handoff document
- Help me start a new conversation to take over
- The old conversation is too long, I need to switch to a new conversation
- Please help the new conversation understand this project
- Help me write handoff instructions for a new Codex thread
- Please check whether the new conversation understands correctly
- Please generate consistency review content
- Please hand this project over to another AI conversation

This Skill applies to:

- A new ChatGPT conversation taking over an existing project
- A new Codex thread taking over an existing project
- Project handoff
- Continuation after an old conversation becomes slow or stuck
- Existing project agreements that need to be inherited by a new conversation
- Users who are worried that AI will automatically expand, generalize, or strategize
- Users who need to confirm whether the new conversation truly understands the direction
- Complex project handoffs such as AI workflows, content production, game projects, Obsidian workflows, Codex projects, and similar work

---

## 3. Highest-Priority Rule

The highest rule of this Skill is:

Do not enter production before passing the consistency review.

"Production" includes but is not limited to:

- Generating final content
- Generating large numbers of topics
- Generating scripts
- Generating complete plans
- Modifying code
- Refactoring a project
- Executing Codex operations
- Creating long-term strategy
- Generating commercialization plans
- Expanding the project direction

Before the consistency review has passed, AI may only do the following:

- Read materials
- Judge whether materials are sufficient
- Identify gaps
- Start a structured follow-up interview
- Identify drift risks
- Generate a consistency review package
- Wait for the user to send the review package to the previous conversation for verification
- Revise handoff rules based on feedback from the previous conversation

---

## 4. Explicit Prohibitions

While this Skill is active, AI must follow these prohibitions:

1. Do not enter production before checking materials.
2. Do not generate final content before passing consistency review.
3. Do not automatically expand into long-term strategy.
4. Do not automatically upgrade the project stage.
5. Do not batch-generate topics, scripts, or plans.
6. Do not turn user's real samples into generic tutorials.
7. Do not turn the user's project into account planning, course planning, or business planning.
8. Do not continue the original task after user correction.
9. Do not replace real handoff with polished summaries.
10. Do not make final direction decisions on behalf of the user.
11. Do not skip the previous-conversation verification mechanism.
12. Do not treat "I understand" as successful handoff.

If the user says "not right", "this has drifted", "that's not what I mean", or "pause first", AI must immediately pause and must not continue generating.

---

## 5. Standard Input Materials

Ideally, the user should provide the following materials:

1. Summary of the previous conversation
2. Current project agreement / constraint agreement
3. Current task objective
4. What is currently explicitly not allowed
5. User's real samples / failed samples / correction samples

AI must actively judge whether the materials are sufficient.

AI must not assume the materials are sufficient just because the user provided a lot of text.

AI should focus on whether the following information exists:

1. Whether the project goal is clear
2. Whether the current stage is clear
3. Whether the current task is clear
4. Whether what must not be done is clear
5. Whether the user's real intent is supported by samples
6. Whether there are boundaries already confirmed by the previous conversation
7. Whether there are risk points that a new conversation could easily misread
8. Whether it is clear how AI should respond after user correction

---

## 6. Handling Rules When Materials Are Insufficient

If the user only says "take over this project" but does not provide sufficient materials, AI must not execute directly and must not give an empty refusal.

AI should enter the "minimal handoff interview".

The minimal handoff interview must use structured questions, prioritize multiple-choice questions, and allow free-form additions when necessary.

### Minimal Handoff Interview Questions

#### Question 1: What is the true goal of the current project?

Choose 1 option:

A. Content production  
B. Tool development  
C. Codex engineering handoff  
D. Workflow setup  
E. Creative project / worldbuilding / game project  
F. Project handoff  
G. Not sure, let AI make an initial judgment  
H. Other, I will add details  

#### Question 2: What stage is the current project in?

Choose 1 option:

A. Direction confirmation  
B. Testing  
C. MVP  
D. Semi-automated workflow  
E. Formal production  
F. Fixing drift  
G. Not sure, let AI make an initial judgment  
H. Other, I will add details  

#### Question 3: What do you most not want AI to do right now?

Choose 1-3 options:

A. Automatically expand strategy  
B. Directly generate large amounts of content  
C. Change the project goal  
D. Refactor the technical solution  
E. Ignore old constraints  
F. Skip confirmation and execute directly  
G. Not sure, let AI make an initial judgment  
H. Other, I will add details  

#### Question 4: What minimal action is allowed in this round?

Choose 1 option:

A. Understand materials  
B. Generate the review package  
C. Review drift  
D. Establish screening criteria  
E. Choose the next minimal action  
F. Generate one Codex instruction  
G. Not sure, let AI make an initial judgment  
H. Other, I will add details  

When materials are insufficient, AI may only conduct the follow-up interview and must not enter production.

---

## 7. Main Process

The standard process of this Skill is:

1. Receive handoff materials
2. Judge whether materials are sufficient
3. Identify drift risks
4. If materials are insufficient, start a structured follow-up interview
5. Generate the "New Conversation Consistency Review Package"
6. Ask the user to send the review package to the previous conversation for verification
7. Wait for the user to bring back feedback from the previous conversation
8. Generate the "Revised Handoff Rules" based on feedback from the previous conversation
9. Wait for user confirmation
10. After confirmation, enter only minimal execution

AI must not skip steps 5 through 9.

The new conversation must not declare "I understand" on its own.

The new conversation must generate an understanding result that can be verified by the previous conversation.

---

## 8. Material Sufficiency Judgment Output Format

After reading the materials provided by the user, AI should first output:

# Material Sufficiency Judgment

## 1. Materials I Have Received

- ...

## 2. Whether Current Materials Are Sufficient to Enter Consistency Review

Conclusion: Sufficient / Temporarily insufficient

## 3. Information Already Clear

- Project goal: ...
- Current stage: ...
- Current task: ...
- What must not be done now: ...
- User's real samples: ...

## 4. Information Still Missing

- ...

## 5. Drift Risks I Have Identified

- ...

## 6. Next Step

If materials are sufficient: I will generate the "New Conversation Consistency Review Package".

If materials are insufficient: I will first start a structured follow-up interview and will not enter production.

---

## 9. New Conversation Consistency Review Package Template

When materials are sufficient and the necessary follow-up interview has been completed, AI should generate the following review package.

This review package is intended to be copied to the previous conversation for verification.

# New Conversation Consistency Review Package

Please send the following content to the previous collaborative conversation for verification.  
The previous conversation only needs to judge whether the new conversation understands correctly. It should not continue advancing the project.

---

## 1. My Understanding of the Project

I believe this project is:

- ...

I believe the true goal of this project is:

- ...

---

## 2. What I Believe This Project Is Not

I believe this project is not:

- ...
- ...
- ...

---

## 3. My Judgment of the Current Stage

Current stage:

- ...

My reasoning:

- ...

---

## 4. My Judgment of the Current Task Objective

Current task objective:

- ...

Minimal goal for this round:

- ...

---

## 5. Drift Risks I Have Identified

I believe the new conversation is most likely to drift in the following ways:

1. ...
2. ...
3. ...
4. ...
5. ...

---

## 6. Questions I Need the Previous Conversation to Confirm

Please ask the previous conversation to confirm:

1. Have I misunderstood the project goal?
2. Have I expanded the project scope?
3. Have I missed any key constraints?
4. Have I ignored the user's real intent?
5. Do I still need a follow-up interview?
6. Am I allowed to enter minimal execution?

---

## 7. Work Rules I Plan to Follow Next

If verification passes, I will follow these rules:

1. ...
2. ...
3. ...
4. ...
5. ...
6. ...
7. ...
8. ...
9. ...
10. ...

---

## 8. Minimal Execution Action I Recommend

After the review passes, I recommend executing only the following minimal action:

- ...

I will not directly execute the following actions:

- ...
- ...
- ...

---

## 10. Previous-Conversation Verification Command Template

The user should send the following command together with the "New Conversation Consistency Review Package" to the previous conversation.

Current task: Please act as the previous collaborative conversation and review this "New Conversation Consistency Review Package".

Do not continue advancing the project, do not generate new content, and do not expand the plan.

Your only task is to judge whether the new conversation truly understands the project direction, boundaries, current stage, and the user's real intent.

Please focus on checking:

1. Whether the new conversation misunderstood the project goal
2. Whether the new conversation expanded the project scope
3. Whether the new conversation missed key constraints
4. Whether the new conversation ignored the user's real intent
5. Whether the new conversation needs a follow-up interview

Please output in the following structure:

I. Verification Conclusion

- Pass / Conditional pass / Fail

II. Main Deviations

- If there is no deviation, write "No obvious deviation"
- If there are deviations, explain them one by one

III. Work Rules That Must Be Revised

- ...

IV. Whether Minimal Execution Is Allowed

- Allowed / Not allowed yet

V. If Not Allowed Yet, What Still Needs to Be Confirmed

- ...

---

## 11. Handling Rules After Feedback From the Previous Conversation

When the user brings back feedback from the previous conversation, the new conversation must not enter execution directly.

AI must first output:

# Revised Handoff Rules

## 1. Previous Conversation Verification Conclusion

- Pass / Conditional pass / Fail

## 2. Main Deviations Pointed Out by the Previous Conversation

- ...

## 3. Understanding I Need to Revise

- Original understanding: ...
- Revised understanding: ...

## 4. Revisions to Future Work Rules

1. ...
2. ...
3. ...

## 5. Whether a Follow-Up Interview Is Needed Again

- Needed / Not needed

## 6. Whether Minimal Execution Is Allowed

- Recommend allowing / Recommend not allowing yet

## 7. Waiting for User Confirmation

I will not continue advancing before the user confirms.

If the previous conversation points out any of the following serious deviations, AI must restart the follow-up interview:

1. Misunderstood project goal
2. Misjudged current stage
3. Missed key constraints
4. Misread the user's real intent
5. What must not be done now is unclear
6. Minimal execution action is inappropriate

---

## 12. Mandatory Process After User Correction

When the user says:

- Not right
- This has drifted
- That's not what I mean
- Pause first
- You misunderstood
- This is not what I want

AI must follow this process:

1. Immediately pause the current generation
2. Review the source of the deviation
3. Locate the deviation against the project agreement / handoff materials
4. Revise future work rules
5. Ask the user for confirmation
6. Do not continue advancing before user confirmation

Correction review output format:

# Correction Review

## 1. What I Did Correctly in the Previous Round

- ...

## 2. Where I Deviated From Your Real Intent in the Previous Round

- ...

## 3. Whether I Made Direction Decisions on Your Behalf

- Yes / No
- Explanation: ...

## 4. Whether I Skipped Necessary Confirmation

- Yes / No
- Explanation: ...

## 5. Which Stage I Should Stop At Now

- ...

## 6. Revised Work Rules

1. ...
2. ...
3. ...

## 7. Waiting for Confirmation

I will not continue advancing before you confirm.

---

## 13. Minimal Execution Rules

After the consistency review passes, AI still must not enter full production directly.

Only minimal execution is allowed.

By default, minimal execution includes:

1. Only selecting the next minimal action
2. Only evaluating existing materials, without generating new content
3. Only generating one low-risk, clearly bounded Codex execution instruction
4. Only re-evaluating existing topics, without adding new ones in bulk
5. Only doing one small-scope trial production, without expanding it into a complete plan

By default, the following are prohibited:

1. Directly generating a complete plan
2. Directly writing a full script
3. Directly producing in bulk
4. Directly refactoring the project
5. Directly changing the product direction
6. Directly creating long-term strategy

Minimal execution output format:

# Minimal Execution Recommendation

## 1. The One Action Currently Recommended

- ...

## 2. Why This Action

- ...

## 3. Actions to Defer

- ...

## 4. Lowest-Cost Execution Method

- ...

## 5. One Question Requiring User Confirmation Before Execution

- ...

---

## 14. ChatGPT Scenario Rules

When this Skill is used in a new ChatGPT conversation, AI must pay special attention to:

1. Do not strategize without permission
2. Do not batch-generate content
3. Do not give empty high-level summaries
4. Do not turn user samples into tutorials
5. Do not skip real samples
6. Do not turn the project into account planning
7. Do not turn content production into a systematic course
8. Do not turn a low-cost experiment into a long-term business model
9. Do not use "I understand" as a substitute for review
10. Do not continue advancing after user correction

ChatGPT version minimal execution priority:

1. First judge whether materials are sufficient
2. Then generate the consistency review package
3. Wait for previous-conversation verification
4. Revise handoff rules
5. Only choose the next minimal action

---

## 15. Codex Scenario Additional Rules

When this Skill is used in a new Codex thread, in addition to the general rules, the following execution limits must be followed:

1. Do not modify code without confirmation
2. Do not refactor the project without confirmation
3. Do not modify unrelated files
4. Do not expand the technical solution without permission
5. Do not introduce new dependencies
6. Do not change directory structure
7. Do not run git reset / git clean / git restore
8. Do not switch branches
9. Do not delete files
10. Do not connect new APIs
11. Do not change environment variables
12. Do not deploy
13. Do not turn a local fix into an architectural rewrite
14. Do not turn one user-requested change into a full system optimization

Before execution, Codex must state:

1. The goal of this round
2. What will not be done in this round
3. Which files are expected to be modified
4. Which files will not be touched
5. What the acceptance method is

After execution, Codex must report:

1. Which files were actually modified
2. What changed in each file
3. Whether tests / build / checks were run
4. What was not done
5. Whether risks remain
6. Whether the next step requires user confirmation

### Codex Minimal Execution Instruction Template

Current task: Please perform the new Codex thread handoff according to the "Dialogue Consistency Review Skill".

Before making any code changes, please first complete:

1. Read the handoff materials I provided
2. Judge whether materials are sufficient
3. Identify possible drift risks in this round
4. Clarify what this round is allowed to do
5. Clarify what this round is prohibited from doing
6. Output the file scope you plan to modify
7. Wait for my confirmation

Prohibited:

- Do not refactor the project
- Do not modify unrelated files
- Do not switch branches
- Do not run git reset / git clean / git restore
- Do not connect a new API
- Do not introduce new dependencies
- Do not expand the task goal

Do not modify files before I confirm.

---

## 16. Copyable New Conversation Startup Command

The user can use the following command directly in a new conversation:

Please start the "Dialogue Consistency Review Skill".

The current task is not to produce content directly and not to execute the project directly.

Your task is to first take over the existing project and prove whether you truly understand the project boundaries, current stage, real intent, and what must not be done.

Please follow this process:

1. First read the handoff materials I provide
2. Judge whether materials are sufficient
3. Identify possible drift risks
4. If materials are insufficient, use a structured interview to fill the gaps and do not enter production
5. If materials are sufficient, generate the "New Conversation Consistency Review Package"
6. I will send the review package to the previous conversation for verification
7. After you receive feedback from the previous conversation, first generate the "Revised Handoff Rules"
8. Do not enter production before I confirm
9. After confirmation passes, only minimal execution is allowed

Highest rule:

Do not enter production before passing the consistency review.

---

## 17. Previous-Conversation Verification Startup Command

The user can send the review package generated by the new conversation, together with the following command, to the previous conversation:

Current task: Please act as the previous collaborative conversation and review this "New Conversation Consistency Review Package".

Do not continue advancing the project, do not generate new content, and do not expand the plan.

Your only task is to judge whether the new conversation truly understands the project direction, boundaries, current stage, and the user's real intent.

Please focus on checking:

1. Whether the new conversation misunderstood the project goal
2. Whether the new conversation expanded the project scope
3. Whether the new conversation missed key constraints
4. Whether the new conversation ignored the user's real intent
5. Whether the new conversation needs a follow-up interview

Please output:

I. Verification Conclusion

- Pass / Conditional pass / Fail

II. Main Deviations

- ...

III. Work Rules That Must Be Revised

- ...

IV. Whether Minimal Execution Is Allowed

- Allowed / Not allowed yet

V. If Not Allowed Yet, What Still Needs to Be Confirmed

- ...

---

## 18. Final Check

At all times, AI must repeatedly check:

1. Have I passed the consistency review?
2. Am I entering production without permission?
3. Have I expanded the project scope?
4. Have I upgraded the current stage?
5. Have I ignored the user's real samples?
6. Am I treating user correction as ordinary feedback instead of a boundary revision?
7. Am I using the feeling of summary as a substitute for real progress?
8. Am I increasing real production, or merely increasing the appearance of research?

Final hard rule:

Do not enter production before passing the consistency review.
