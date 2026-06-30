# Handoff Reference

## Handoff Package Minimum

When handing materials to another thread, include:

- task objective
- source platform and source link description, with sensitive parameters removed
- local root directory
- human entrance path if available
- thread entrance path if available
- raw/source paths
- transcript/OCR/comment status
- what has not been done
- what the receiving thread is allowed to do
- what it must not do
- expected return format

## Execution Thread Prompt Shape

Use explicit constraints:

```text
你是【执行线程名称】。

任务：
1.
2.

输入目录：

输出目录：

必须遵守：
- 不移动、删除、重命名原始文件。
- 不写 Obsidian、PromptCopyPanel、全局规则或正式 Skill。
- 不读取、输出、保存 cookie/token/密钥。
- 中文文件 UTF-8。

完成后回报：
- 产物路径
- 处理数量
- 失败项
- 不确定点
- 下一步建议
```

## Controller Acceptance

After an execution thread returns:

1. Verify paths exist.
2. Check obvious encoding problems.
3. Confirm it did not exceed boundaries.
4. Convert the result into user-facing status.
5. Decide whether further analysis, project handoff, or only preservation is needed.

## Reporting Style

Keep reports short and checkable:

- what changed
- where to open it
- what is still pending
- what is uncertain
- what should happen next

