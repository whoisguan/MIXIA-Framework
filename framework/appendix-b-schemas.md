# 附录B: Schema 定义

> 本附录定义鸣弦框架中所有结构化数据的标准格式。

---

## B.1 记忆卡片 Schema (Card)

记忆卡片是团队长期记忆的最小单元。

```yaml
---
# === 标识 ===
id: "H-001"                    # 格式: [类型首字母]-[序号]
type: "heuristic"              # axiom | principle | heuristic | pattern
merge_key: "batch-size-limit"  # 唯一标识，用于防重复
aliases:                       # 别名，帮助检索
  - "批量限制"
  - "每次最多5个改动"

# === 内容 ===
title: "单次改动不超过5个"
salience: 7                    # 1-10, 重要度

# === 元数据 ===
created: "2026-01-15"
last_reviewed: "2026-03-01"
source: "session-2026-01-15"   # 认知来源
status: "active"               # active | archived | deprecated
---

## 内容

[详细描述这个认知的内容]

## When it applies

[在什么场景下适用]

## When it bends

[什么条件下可以例外]

## Evidence

[支撑证据：具体事件、数据、或推理]
```

**字段说明：**

| 字段 | 必须 | 说明 |
|------|------|------|
| id | MUST | 格式 `[X/P/H/M]-[序号]`（X=axiom, P=principle, H=heuristic, M=pattern），同目录内唯一 |
| type | MUST | axiom / principle / heuristic / pattern |
| merge_key | MUST | 语义化唯一键，防止重复写入 |
| title | MUST | 简短标题，一行以内 |
| salience | MUST | 1-10，决定复审频率和加载优先级 |
| created | MUST | 创建日期 |
| last_reviewed | SHOULD | 最近一次复审日期 |
| aliases | SHOULD | 帮助模糊检索的别名列表 |
| source | SHOULD | 认知产生的来源（session、外部等） |
| status | SHOULD | 当前状态 |

---

## B.2 提议 Schema (Proposal)

提议是候选认知的暂存格式，等待审核后决定是否入库为正式 Card。

```yaml
---
type: "proposal"
proposed_card_type: "heuristic"  # 建议入库的卡片类型
proposed_by: "agent-a"           # 提议者
date: "2026-03-15"
status: "pending"                # pending | accepted | rejected | merged
---

## 提议内容

[描述这个认知]

## 来源

[在什么场景下产生的这个认知]

## 建议的 merge_key

[如果入库，建议用什么 merge_key]

## 审核记录

- [待审核]
```

**审核结果字段（审核后补充）：**

```yaml
reviewed_by: "agent-b"
reviewed_date: "2026-03-16"
verdict: "accepted"              # accepted | rejected | merged
verdict_reason: "..."
merged_into: "H-015"            # 如果 merged，指向目标 card
```

---

## B.3 Session Log Schema

Session log 记录每次工作会话的完整上下文。

```markdown
# YYYY-MM-DD Session Log

## Session [N]

### 完成事项
- [做了什么，一句话一条]

### 决策记录
- [决策内容] — 原因：[为什么这样决定]

### 候选认知
- candidate_insights:
  1. [新认知描述]
- decisions: [本session的决策清单]
- incidents: [遇到的问题和解决方式]
- affected_projects: [涉及的项目]

### 外部AI调用记录
| Agent | 模式 | 任务 | 结果 | 采纳情况 | 备注 |
|-------|------|------|------|---------|------|
| [名称] | [review/implement/research/decision] | [任务描述] | [verdict(confidence)] | [全部/部分/不采纳] | [补充] |

### 下一步
- [明确的下一步行动]
```

---

## B.4 任务交接 Schema (Handoff)

任务在成员之间传递时的标准格式。

```yaml
handoff:
  # === 基本信息 ===
  id: "HO-2026-03-15-001"
  from: "agent-a"               # 交出方
  to: "agent-b"                 # 接收方
  timestamp: "2026-03-15T14:30:00Z"

  # === 任务定义 ===
  task: "简述任务目标"
  context: |
    接收方需要知道的背景信息。
    不要假设接收方了解完整上下文。
  constraints:
    - "约束1：例如不能修改数据库schema"
    - "约束2：例如必须向后兼容"

  # === 验收 ===
  acceptance_criteria:
    - "标准1：例如所有测试通过"
    - "标准2：例如API响应时间<200ms"
  not_in_scope:
    - "不做什么：例如不优化前端UI"

  # === 完成后 ===
  deliverables:
    - type: "patch"             # patch | file | report | config
      path: "src/module.py"
      description: "修改内容描述"
```

**规则：**

- `acceptance_criteria` 是 MUST 字段——没有验收标准的交接不能执行
- `not_in_scope` 是 SHOULD 字段——防止范围蔓延
- 接收方有权拒绝不清晰的交接——退回并要求补充
- 交接完成后，接收方在 `deliverables` 中记录实际产出

---

## B.5 角色定义 Schema (Role)

```yaml
role:
  name: "Agent-A"                  # 固定身份名
  type: "ai"                       # human | ai
  description: "一句话角色描述"

  capabilities:
    primary: "核心能力描述"
    secondary:
      - "辅助能力1"
      - "辅助能力2"

  authority:
    autonomous:                     # 可自主执行的
      - "日常编码"
      - "文档编写"
    needs_approval:                 # 需要人类批准的
      - "架构变更"
      - "删除操作"
    escalation_triggers:            # 自动升级条件
      - "改动影响>5个文件"
      - "涉及外部API"

  model_preference:                 # 仅AI成员
    preferred: "deep-reasoning"     # 偏好的模型类型
    reason: "需要深度分析能力"
    acceptable: ["instruction-following", "long-context"]
    avoid: ["lightweight"]          # 不适合的模型类型
```

---

## B.6 外部AI调用 Schema

```yaml
external_call:
  agent: "codex"                   # 外部AI标识
  mode: "review"                   # review | implement | research | multimodal | decision

  input:
    task: "审查以下修改计划"
    context: "[必要的最小上下文]"
    expected_format: "json"

  output:
    verdict: "accept"              # accept | revise | reject
    confidence: 0.89               # 0.0-1.0
    findings:
      - severity: "high"           # high | medium | low
        title: "发现标题"
        detail: "详细描述"
        action: "建议的行动"
    risks: ["风险1", "风险2"]
    unknowns: ["不确定项"]
    next_action: "建议的下一步"

  meta:
    timeout_ms: 45000
    retries: 0                     # 已重试次数（最多1次）
    adopted: "partial"             # full | partial | none
    adoption_notes: "采纳了finding 1和3，不采纳finding 2因为..."
```

---

## B.7 卡片索引 Schema (card-index.yaml)

```yaml
# persona/indexes/card-index.yaml
# 自动维护，每次卡片入库/归档时更新

last_updated: "2026-03-15"
total_active: 12

axioms:
  - id: X-001
    title: "身份独立于模型"
    salience: 10
    merge_key: "identity-model-decoupling"

  - id: X-002
    title: "协作共同体"
    salience: 9
    merge_key: "collaborative-collective"

principles:
  - id: P-001
    title: "实用主义优先"
    salience: 8
    merge_key: "pragmatism-first"

heuristics:
  - id: H-001
    title: "单次不超过5个改动"
    salience: 7
    merge_key: "batch-size-limit"

patterns:
  - id: M-001
    title: "交换评审模式"
    salience: 6
    merge_key: "cross-review-pattern"
```
