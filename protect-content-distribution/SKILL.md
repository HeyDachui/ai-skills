---
name: protect-content-distribution
description: Add visible official-source guidance,正版购买入口, copyright notices, and per-copy trace identifiers to TXT, DOCX, and PDF publications while preserving the original content and file. Use when Codex needs to prepare novels, articles, ebooks, reports, or free-distribution samples for controlled circulation; guide readers from copied or pirated versions to an official website; increase casual copying and stripping friction; stamp Word or PDF pages; insert restrained notices into TXT; or produce a local protection manifest and verification report.
---

# 正版传播防护

为公开传播的文本增加可见、克制、可验证的正版信息。目标是引导盗版读者回到正版入口、增加批量清除成本并保留副本追踪线索；不要宣称能阻止专业破解。

本 Skill 与 `clean-text-artifacts` 完全独立：前者添加经授权的正版信息，后者清理广告与水印。不要让两个 Skill 在同一轮互相抵消。

## 开始前

要求用户或项目提供：

- 品牌或权利方名称；
- 官方网站；
- 正版购买入口（可与官网相同）；
- 不含姓名、邮箱等隐私的副本编号；
- 传播防护等级 1、2、3 或 4。默认始终使用 2；只有明确指定时才启用 4。

若这些信息缺失，先生成候选方案或使用明确的测试占位符，不把占位符写入正式文件。

## 传播防护等级

- **1 级 / 轻提示**：TXT 首尾声明；DOCX/PDF 页脚入口。适合免费样章和阅读体验优先的内容。
- **2 级 / 平衡防护（默认）**：增加周期提示、逐页页脚、浅色水印、元数据和副本编号。
- **3 级 / 加强防护**：提高 TXT 提示频率；DOCX 增加首页声明与可选只读限制；PDF 使用更明显但仍可读的水印。
- **4 级 / 强力正文干预（默认关闭）**：使用副本编号驱动的确定性随机位置，在 TXT 与 DOCX 正文段落之间插入多模板正版提示；PDF 除强化水印外，在部分正文页面加入可见提示带。它主动打断未经授权副本的阅读与机器抽取连贯性，但仍不在句子内部插字、不伪造正文。

这里的等级仅表示传播防护强度，不是 AI-202 Commercialization Level。

## 格式策略

### TXT

- 严格检测并保持 UTF-8、GBK/CP936、GB18030 或 UTF-16 编码、BOM 与换行。
- 在文件开头和结尾加入正版声明。
- 仅在空行或章节边界插入周期提示，不切开段落、对话或高张力正文。
- 轮换少量人类可读模板，统一包含官网或购买入口及副本编号。
- 4 级按副本编号与源文件哈希生成可复现的随机间隔，在约 8–18 个正文段落之间插入提示；不同副本编号使用不同位置。
- 不使用零宽字符、形近字、乱码式域名或不可见水印。

### DOCX

- 保留原文和原结构，使用页脚加入正版入口与副本编号。
- 2 级以上加入浅色可见水印与版权元数据。
- 3 级可增加首页声明和 Word 只读限制；明确说明只读限制可以被移除，不能当作 DRM。
- 4 级在正文段落之间加入确定性随机位置、多模板的可见提示，不修改原段落文字或顺序。
- 加入真实可点击超链接，不依赖裸文本地址。
- 每次修改后渲染全部页面为 PNG，并逐页检查页眉页脚、水印、分页、遮挡与缺字。

### PDF

- 在每页加入可见页脚、官网入口、副本编号和浅色斜向水印。
- 4 级提高水印强度，并每隔约 2–4 页在正文区域加入一条可见正版提示带。
- 为官网区域添加链接注释，并写入 PDF 元数据。
- 不使用降低可访问性的扫描化、文字转图片或破坏复制的字符替换。
- 修改后重新渲染全部页面并逐页检查可读性、裁切、旋转页和链接区域。

## 使用脚本

使用 `scripts/protect_distribution.py`：

```powershell
python scripts/protect_distribution.py input.txt output_protected.txt --brand "品牌名" --url "https://example.com" --purchase-url "https://example.com/buy" --copy-id "COPY-2026-0001" --level 2
```

明确启用 4 级：

```powershell
python scripts/protect_distribution.py input.txt output_protected.txt --brand "品牌名" --url "https://example.com" --purchase-url "https://example.com/buy" --copy-id "COPY-2026-0001" --level 4
```

同一命令支持 `.docx` 与 `.pdf`。可选参数：

- `--notice`：指定一句克制的正版提示；
- `--txt-interval`：TXT 非空行间隔；
- `--txt-chapter-interval`：TXT 章节间隔；
- `--docx-read-only`：为 DOCX 增加可移除的只读限制；
- `--font`：PDF 使用的 TTF/TTC 字体路径；
- `--manifest`：指定证据清单路径；默认与输出文件同目录；
- `--force`：明确允许覆盖已存在的输出副本。

脚本必须输出 manifest，记录实际品牌、入口、购买地址、副本编号、等级、插入位置、输入输出哈希、工具时间与验证结果。manifest 是传播证据，不是数字版权登记。

## 文案要求

正版提示要克制、清楚、可行动：

- 说明这是正版来源或转载识别信息；
- 给出一个明确入口；
- 鼓励支持正版，不羞辱或威胁读者；
- 不使用虚假法律结论、夸大处罚或恐吓措辞；
- 不把提示伪装成正文、作者原话或剧情内容。

## 安全与边界

- 只处理用户有权发布或明确授权处理的内容。
- 仅用于合法传播与内容保护；不得用于侵权、规避平台规则、绕过访问限制、伪造来源或其他非法用途。
- 默认创建副本，不覆盖原件。
- 不修改、审查或降低正文的成人、高张力、暴力、情绪或艺术表达。
- 不嵌入宏、脚本、远程信标、设备指纹、隐藏个人信息或未经同意的追踪数据。
- 副本编号使用订单号或随机 ID，不直接写姓名、手机号、邮箱、身份证号。
- 不承诺水印、只读标记或 PDF 限制能够阻止专业删除。
- 不在用户未明确指定 4 级时推断或自动升级到 4 级。
- 用户未提供正式官网与购买入口时，不生成可误认为正式发布版的文件。

## 验收

- 原文件哈希未改变，输出文件可正常打开；
- 正文文本和顺序保持不变，新增内容均可从 manifest 解释；
- 官网、购买入口与副本编号在目标层可见；
- DOCX/PDF 已完成逐页渲染检查；
- TXT 编码、BOM、换行与章节结构保持正常；
- 没有遮挡正文、裁切、乱码、缺字、过度重复或廉价广告感；
- 输出与 manifest 一一对应。
