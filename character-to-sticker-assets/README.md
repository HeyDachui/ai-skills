# skill整理员｜表情包 Skill（character-to-sticker-assets）

把一个人物、宠物、品牌吉祥物或已有角色，从一张参考图发展成一套身份稳定、能继续扩展的表情资产。

账号／内容来源：`skill整理员`

中文展示名：`skill整理员｜表情包 Skill`
机器调用名：`$character-to-sticker-assets`

中文名用于界面、文档和对外介绍；机器调用名保留稳定的英文连字符 slug，以兼容 GitHub 目录和支持 Skill 的客户端发现机制。

## 公开入口

- 规范 slug：`character-to-sticker-assets`
- 中文名：`角色转表情包资产`
- 发布账号：`HeyDachui`
- 官方仓库：[HeyDachui/ai-skills](https://github.com/HeyDachui/ai-skills)
- 本 Skill 目录：[character-to-sticker-assets](https://github.com/HeyDachui/ai-skills/tree/main/character-to-sticker-assets)
- 主入口：[SKILL.md](SKILL.md)
- 调用元数据：[agents/openai.yaml](agents/openai.yaml)

## 它解决什么

- 零基础用户不知道从哪里开始时，先用普通语言逐轮引导；
- 为每个角色绑定唯一母版，降低跨表情、跨视角和跨 AI 的身份漂移；
- 先做 1—3 张高信息量小样，再扩展整套表情、双角色互动、动画和平台交付；
- 把“角色身份、动作参考、场景参考、真实可编辑源”分开；
- 用真实使用尺寸、透明度、源文件真实性和状态标签判断结果，不把文件存在说成已采用或平台通过。

## 使用

将整个 `character-to-sticker-assets` 目录复制到支持 Skill 文件夹的 AI 客户端，再调用 `$character-to-sticker-assets`。`SKILL.md`、`agents/`、`references/` 和 `assets/templates/` 需要一起保留；只复制主文件会缺少访谈、提示词记录和质量门禁入口。

如果已有角色图，请把它标为身份参考；如果还要借鉴动作或场景，请分别说明每张参考图的职责。新角色、新表情、新动作和新视角必须由图像生成能力完成；只有真实同版本 PSD、ORA 等可编辑源文件才允许按用户要求直接编辑。

## 公开版案例边界

本 Skill 保留三个文字案例：白猫、黑猫和红围巾女孩，分别用于学习双角色互动、母版／拆件／动态边界和人形角色扩展。公开版不包含内部生成图片、GIF、ORA 源文件、对话记录、项目证据或本地路径；请使用你有权使用的角色素材。

案例名称仅用于方法说明，不表示 DeepSeek、ChatGPT 或任何其他平台的背书、授权或角色权利转移。

## 限制

这是角色表情资产工作流，不是自动爆款生成器、平台审核保证或权利清查服务。平台参数、授权条件和公开发布要求应在真实提交前按目标平台和具体素材单独核对。

## 许可证与来源

本公开版包含原创方法说明、接口元数据、通用模板和脱敏文字案例说明；不包含内部生产资产或第三方源文件。按 [CC BY 4.0](LICENSE.md) 发布，改编或再分发时请保留署名、许可证链接并注明改动。完整边界见 [NOTICE.md](NOTICE.md) 和 [MANIFEST.json](MANIFEST.json)。
