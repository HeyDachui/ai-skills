---
name: handoff-to-next-person
description: "Use when an AI beginner explicitly wants another person, AI assistant, or new chat to continue an existing task. Do not use for internal task creation, background job control, or ordinary final delivery. Produce a short copyable handoff with the goal, materials, current result, next action, and anything that must not change."
---

# 换人不丢信息 / Handoff to the Next Person

当使用者要换一个人、AI或新对话继续时，整理一段短交接，让接手者不用重新猜。

When the user moves to another person, AI assistant, or chat, create a short handoff so the next helper can continue without guessing.

## 怎么做 / What to do

1. 只保留继续工作真正需要的信息：目标、材料、已经做到哪里、下一步和不能改的内容。  
   Keep only the goal, materials, current result, next action, and anything that must not change.
2. 使用可复制的普通语言，不使用内部治理、线程管理或审批术语。  
   Use copyable ordinary language, not internal governance or workflow jargon.
3. 省略空字段，不粘贴长日志、密钥、隐私材料或整段历史对话。  
   Omit empty fields and do not paste long logs, secrets, private data, or the full chat history.
4. 只有缺少关键材料会让接手者无法继续时，才问一个问题。  
   Ask one question only if missing material prevents continuation.

## 默认交接 / Default handoff

```text
请继续完成：
现有材料：
已经做到：
下一步：
不要改：
完成时请给我：
```

```text
Please continue:
Materials:
Current result:
Next step:
Do not change:
When done, give me:
```

默认控制在一屏内；复杂任务再按需要补充。

Keep the default handoff within one screen and add detail only when the task truly needs it.
