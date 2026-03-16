# 附录C: 通用案例 Walkthrough

> 本附录通过一个完整的虚构案例，展示鸣弦框架从接收需求到完成交付的全链路。

---

## 场景设定

- **团队：** 一位产品经理（人类）+ 两位AI成员（Alpha=策划, Beta=实现）
- **项目：** 一个内部管理系统
- **任务：** 给系统添加"员工自评"功能

---

## Phase 1: Boot（启动）

Alpha（策划AI）在新 session 开始时执行 Boot 流程：

```
[1] 读取 core/boot.md
    → "我是 Alpha，负责架构设计和方案评估。人类成员偏好先讨论逻辑再动手。"

[2] 读取 core/principles.md
    → P1: 先跑起来再优化（MVP优先）
    → P2: 系统设计必须考虑使用者感受
    → P3: 永远验证，不信"已完成"

[3] 读取 core/challenge-core.md
    → 加载挑战触发条件

[4] 读取 sessions/2026-03/2026-03-20.md
    → "上次完成了员工列表页面。下一步：员工自评功能。"

[5] 读取 .alpha/private/
    → [私有笔记：上次人类成员在疲劳状态下做了几个决策，今天注意观察]

[6] Ready
```

Alpha 输出启动报告：

```
Session 已启动。
上次进展：员工列表页面完成。
今日待办：员工自评功能。
准备就绪。
```

---

## Phase 2: 需求接收与评估

**人类：** "给系统加个员工自评功能。员工可以填写自评表，主管可以看，年底汇总用。快，今天搞定。"

**Alpha 内部评估：**

```
检测到信号：
  - "快" → 疲劳/时间压力信号 → Challenge Trigger 4
  - "今天搞定" → 可能工作量低估 → Challenge Trigger 5

风险评分：
  +3（涉及权限控制 auth + 数据库新建表 migration）
  +1（涉及3个目录：前端+后端+数据库）
  +1（公共API变更：新增3个端点）
  = 5分 → 必须外部审查，人类确认后才执行

需求拆解：
  1. 数据库：自评表 table
  2. 后端：CRUD API
  3. 前端：自评填写页面
  4. 前端：主管查看页面
  5. 权限：员工只能看自己的，主管能看下属的
  = 5个改动，刚好在批量限制内
```

**Alpha 输出（Challenge 模式触发）：**

```
⚡ 检测到时间压力信号。输出已精简，但关键验证不跳过。

📋 需求拆解（5个改动）：
1. 数据库：新建 self_evaluation 表
2. 后端：自评 CRUD API（4个端点）
3. 前端：员工自评填写页
4. 前端：主管查看下属自评页
5. 权限：行级权限控制

⚠️ 工作量评估：这不是"小改动"。涉及前后端+数据库+权限，
预计需要完整的一个工作session。

🔍 需要确认：
- 自评表的字段有哪些？（自由文本 vs 结构化评分）
- "年底汇总"需要什么格式？
- 权限：主管只能看直属下属，还是可以看整个部门？

⚡ 速度模式：本次决策建议后续review。
```

---

## Phase 3: 方案设计与审查

**人类：** "自由文本就行，3个问题：本年度成就、改进方向、明年目标。主管看直属下属。汇总的事后面再说。"

**Alpha 制定方案并评估风险：**

```
📋 修改计划：

1. 数据库：self_evaluations 表
   - id, employee_id, year, question_key, answer_text, created_at, updated_at
   - 每人每年3条记录（3个问题）

2. 后端 API：
   - GET /api/self-evaluations/mine — 获取自己的自评
   - PUT /api/self-evaluations/mine — 提交/更新自评
   - GET /api/self-evaluations/team — 主管获取下属自评
   - 权限：基于 employee → manager 关系过滤

3. 前端-员工视图：
   - 3个文本框 + 保存按钮
   - 自动加载已有内容（编辑模式）

4. 前端-主管视图：
   - 下属列表 → 点击查看自评（只读）

5. 权限控制：
   - 员工：只能读写自己的
   - 主管：只读直属下属的
   - 无直属关系 = 无权限

风险评分 = 5分（auth/migration +3, 多目录 +1, API变更 +1）
→ ≥4分，必须外部审查 + 人类确认后执行
```

风险分≥4，Alpha **必须**调用外部审查：

```
🔀 多LLM触发（强制）：
任务：自评功能修改计划审查
模式：review
Agent：Beta
风险评分：5分（≥4，强制外审）
原因：涉及权限控制+数据库迁移+公共API，属于高风险改动
```

**人类：** "执行"

**Beta（实现AI）审查结果：**

```json
{
  "verdict": "revise",
  "confidence": 0.88,
  "findings": [
    {
      "severity": "medium",
      "title": "缺少自评提交截止控制",
      "detail": "当前设计允许随时修改自评，但年底汇总时需要'锁定'机制",
      "action": "添加 status 字段（draft/submitted），submitted 后不可修改"
    },
    {
      "severity": "low",
      "title": "question_key 建议用枚举而非自由字符串",
      "detail": "防止前端传入非法问题键",
      "action": "后端校验 question_key ∈ {achievement, improvement, next_year_goal}"
    }
  ],
  "risks": ["如果 manager 关系数据不准确，权限会出错"],
  "next_action": "采纳 findings 后开始实现"
}
```

**Alpha 综合判断：**

```
🔍 Beta 审查结果：

📝 我的判断：
  采纳：
  - ✅ 添加 status 字段（draft/submitted）— 合理，汇总确实需要锁定
  - ✅ question_key 枚举校验 — 好习惯，成本低

  不采纳：无（两条都合理）

调整后的计划已更新。确认执行吗？
```

**人类：** "可以"

---

## Phase 4: 实现

Alpha 将实现任务交接给 Beta：

```yaml
handoff:
  from: alpha
  to: beta
  task: "实现员工自评功能（5个改动）"
  context: |
    方案已确认，含 Beta 自己的审查建议。
    数据库用现有 ORM，前端用现有组件库。
  constraints:
    - "不改现有表结构，只新建表"
    - "权限复用现有 manager 关系数据"
  acceptance_criteria:
    - "员工可以填写、保存、提交自评"
    - "提交后不可修改"
    - "主管可以查看直属下属的已提交自评"
    - "无直属关系的人看不到"
  not_in_scope:
    - "年底汇总功能（后续需求）"
    - "自评提醒通知"
```

Beta 执行实现，完成后返回：

```yaml
deliverables:
  - type: patch
    path: "migrations/add_self_evaluations.sql"
    description: "新建 self_evaluations 表（含 status 字段）"
  - type: patch
    path: "backend/api/self_evaluations.py"
    description: "4个 API 端点 + question_key 枚举校验"
  - type: patch
    path: "frontend/pages/SelfEvaluation.tsx"
    description: "员工自评页面（填写+保存+提交）"
  - type: patch
    path: "frontend/pages/TeamEvaluations.tsx"
    description: "主管查看页面（只读）"
  - type: patch
    path: "backend/middleware/permissions.py"
    description: "权限中间件添加自评相关规则"
```

---

## Phase 5: 验证与提醒

**Alpha 提醒人类验证：**

```
Beta 已完成所有5个改动。

🔍 请在浏览器中验证以下场景：
1. 以员工身份登录 → 填写自评 → 保存草稿 → 提交
2. 提交后尝试修改 → 应该被阻止
3. 以主管身份登录 → 查看该员工的自评
4. 以无关人员登录 → 应看不到他人自评

验证通过后我会记录到 session log。
```

---

## Phase 6: Save（保存）

Session 结束时，Alpha 写入 session log：

```markdown
# 2026-03-21 Session Log

## 完成事项
- 员工自评功能完整实现（数据库+后端+前端+权限）
- Beta 审查发现2个改进点（status字段+枚举校验），已全部采纳

## 决策记录
- 自评表设计：自由文本3个问题，非结构化评分 — 原因：MVP先用最简方案
- 添加 draft/submitted 状态锁定 — Beta 建议，防止汇总时数据不稳定
- 年底汇总功能不在本次范围 — 按人类指示后续再做

## 候选认知
- candidate_insights:
  1. 即使是"简单的CRUD功能"，只要涉及权限就需要完整的方案审查
- decisions: 自评表结构、status锁定机制
- incidents: 无
- affected_projects: 内部管理系统

## 外部AI调用记录
| Agent | 模式 | 任务 | 结果 | 采纳 | 备注 |
|-------|------|------|------|------|------|
| Beta | review | 修改计划审查 | revise(0.88) | 全部采纳 | status字段+枚举校验 |
| Beta | implement | 自评功能实现 | 完成(5文件) | 全部交付 | 验收标准全部满足 |

## 下一步
- 人类浏览器验证自评功能
- 后续需求：年底汇总功能
```

**Alpha 捕获认知信号：**

```
💾 认知收集建议：涉及权限的功能即使看起来简单也需要完整审查 — 需要保存为card吗？
```

**人类：** "存"

Alpha 写入 `proposals/2026-03/proposal-heuristic-permission-review.md`。

---

## 完整链路回顾

```
Boot → 身份恢复 + 上下文加载
  ↓
接收需求 → Challenge 触发（时间压力 + 工作量评估）
  ↓
方案设计 → 风险评分 → 外部审查 → 综合判断
  ↓
任务交接 → 标准 Handoff Schema → 明确验收标准
  ↓
实现 → 按 spec 执行 → 交付 deliverables
  ↓
验证 → 提醒人类浏览器验证
  ↓
Save → Session log + 认知捕获 + proposal 写入
  ↓
Close → 明确下一步
```

**整个过程中：**

- Challenge 模式在接收需求时自动触发，防止盲目执行
- 多LLM审查在风险分≥2时启动，Beta 发现了人类和 Alpha 都没想到的锁定需求
- 任务交接使用标准 schema，确保 Beta 知道做什么、不做什么
- Session log 完整记录决策和外部调用，下次 Boot 可以无缝衔接
- 认知收集在 session 末尾自然发生，低摩擦写入 proposals
