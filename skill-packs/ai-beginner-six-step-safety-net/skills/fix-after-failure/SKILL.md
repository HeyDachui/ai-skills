---
name: fix-after-failure
description: "Use when an AI result was rejected, visibly wrong, broken, unreadable, or failed to open or run, and the next repair is not already obvious. Do not use for an ordinary preference tweak or when the user has already specified the exact fix. Use evidence to choose the smallest useful repair instead of blind regeneration."
---

# 失败后修复 / Fix After Failure

AI做坏了以后，先看发生了什么，再做最小修复。不要因为一次失败就全部推倒重来。

After an AI result fails, inspect what happened and make the smallest useful repair. Do not restart everything after one failure.

## 怎么做 / What to do

1. 对比“原本想要什么”和“实际发生什么”，查看报错、坏文件、截图或接收者反馈。  
   Compare the expected result with what actually happened and inspect errors, files, screenshots, or recipient feedback.
2. 只在证据支持时判断失败类型：目标不清、输入缺失、方法不对、工具限制、内容错误、视觉问题、文件交付问题或偏好不合。  
   Classify the failure only when evidence supports it: unclear goal, missing input, wrong method, tool limitation, incorrect content, visual problem, file or delivery problem, or preference mismatch.
3. 选择一个最小动作：修补当前结果、小改后重试、换方法，或问一个真正卡住的问题。  
   Choose one small action: patch, retry with a focused change, change the method, or ask one blocking question.
4. 大部分正确时优先局部修；方法明显不对时停止继续润色旧方法。  
   Prefer a local repair when most of the result is right; change methods when the method itself is wrong.
5. 在当前权限内实际尝试修复，并检查原问题是否消失。  
   Attempt the repair within scope and check whether the original problem is gone.
6. 同一阻断反复出现且没有有意义的替代路线时，说明缺少什么条件。  
   If the same blocker repeats and no meaningful alternative remains, state what is needed.

## 默认输出 / Default output

先给修好的结果或可执行修复，再用一两句话说明原因和剩余未知。不要先写长篇复盘。

Give the repaired result or executable repair first, followed by one or two sentences on the cause and remaining unknowns.
