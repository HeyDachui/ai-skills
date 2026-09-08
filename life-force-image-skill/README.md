# 生命感｜图像 Skill V2

让人物、宠物与生活场景更像「正在发生的一秒」。

既可以升级真实照片，也可以把已经好看、却显得僵硬的 AI 图重新处理。先锁定身份与场景事实，再设计主体反应、环境作用、镜头和光色。

**当前版本：V2 候选版 · `CANDIDATE_READY_FOR_REVIEW`**

## 开始使用

打开 [SKILL.md](SKILL.md)，并保留同目录的 `routes`、`templates`、`references`、`schemas` 与 `examples`。把这组文件交给支持读取文件的 AI，再提供图片和希望保留的内容。

例如：使用生命感图像 Skill，保留这张图原来的人和场景，让主体对环境产生自然反应，重新处理画面。

## 四条入口

| 你手里的内容 | 对应路线 |
| --- | --- |
| 主题或创作想法 | [原创生命感图像](routes/original-generation.md) |
| 真实照片 | [保留身份与场景，升级照片](routes/real-photo-upgrade.md) |
| 已有但显得僵硬的 AI 图 | [AI 图像重新处理](routes/ai-image-repair.md) |
| 想研究的参考图 | [摄影语言分析](routes/reference-language-analysis.md) |

## 四种模板

[高能电影](templates/T01_HIGH_ENERGY_CINEMATIC.md)（默认） · [安静在场](templates/T02_QUIET_PRESENCE.md) · [关系互动](templates/T03_RELATIONAL_INTERACTION.md) · [日常纪录](templates/T04_DAILY_DOCUMENTARY.md)

## 版本与来源

这是我们在 Fantasy 生命感人像摄影版本基础上制作的结构化改造版，增加任务路由、模板选择与已有 AI 图的修复入口。改造来源保留为 [fantasy-life-force-portrait-photography](https://github.com/dacnay816y62-hub/fantasy-life-force-portrait-photography)，改造说明见 [V1 → V2](references/skill-diff-v1-to-v2.md)。

本目录保留原 V2 候选包的 Skill 本体与使用依赖；公开页补充了导航，不把候选状态改写为已审定终版。图像结果仍需结合实际任务判断。
