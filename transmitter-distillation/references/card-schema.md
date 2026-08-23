# 传承者·蒸馏｜知识卡合同

本文件描述共享蒸馏包的最小语义合同。字段名可映射到其他知识系统，但四层身份不能合并。

## 必填字段

每行一张 JSON 对象，建议写入 `distillation_cards.jsonl`：

```json
{
  "schema": "transmitter.distillation_card.v1",
  "card_id": "artist-topic-001",
  "title": "可复用的中性标题",
  "kind": "mechanism_candidate",
  "problem": "这张卡解决什么创作判断问题？",
  "source_observations": [
    {
      "source_id": "SRC-001",
      "statement": "材料中实际出现的观察，不加作者未说过的结论。"
    }
  ],
  "ai_interpretation": "基于观察形成的解释，明确是 AI 解释。",
  "transferable_mechanism": {
    "principle": "换到其他题目仍可能成立的作用关系。",
    "actions": ["具体动作一", "具体动作二"],
    "diagnostics": ["创作者如何检查是否做到了？"]
  },
  "boundaries": {
    "conditions": ["必须成立的条件"],
    "failure_signals": ["失效时可观察到的信号"],
    "counterexamples": ["限制或反例"],
    "unknowns": ["目前不能据此判断的内容"]
  },
  "trigger_terms": ["用于检索的词"],
  "attribution": {
    "subject": "研究对象",
    "material_identity": "书籍／论文／作品身份"
  },
  "evidence_records": [
    {
      "source_id": "SRC-001",
      "locator": "page:12",
      "excerpt": "足以承载该判断的连续原文或转写。",
      "excerpt_sha256": "由脚本计算的64位十六进制哈希",
      "extraction_method": "native_text|ocr|manual_transcription|other",
      "evidence_role": "它支持哪一条观察或边界？",
      "quality_note": "OCR、缺页或版本差异；没有问题时写清质量正常。"
    }
  ],
  "reading_scope": {
    "covered": "实际读过的章节、页码或时间范围",
    "not_covered": "未读、无法取得或未核对的部分"
  },
  "status": "candidate_only_not_adopted_effect_unknown"
}
```

## 字段边界

- `source_observations` 只能写来源可见内容；不要写“所以作者一定……”。
- `ai_interpretation` 可以有明确观点，但不得冒充作者原话。
- `transferable_mechanism` 写动作、关系、条件和代价，不写词汇模仿。
- `boundaries` 不能只写免责句；要具体说明何时失效和什么证据还缺。
- `evidence_records` 的摘录必须连续，哈希必须对应当前摘录文本。
- `status` 只能表示候选状态，不能写 `adopted`、`effective` 或 `proven`。

## 卡片类型

可使用以下类型，只有正文真正闭合时才使用方法或失败类型：

- `observation_candidate`：材料观察。
- `interpretation_candidate`：由多条观察形成的解释。
- `mechanism_candidate`：具有动作和条件的可迁移机制。
- `criterion_candidate`：可用于审查作品的判断标准。
- `failure_experience_candidate`：带场景、代价和修复方式的失败经验。

“看起来有用”不自动把解释卡升级成方法卡。
