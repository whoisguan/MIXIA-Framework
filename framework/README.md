# 鸣弦/MIXIA Framework

**人与AI协作的团队操作系统**

> "鸣弦而治"——团队成员如琴弦，各自独立振动，共同产生和弦。

---

## 这是什么？

鸣弦/MIXIA 是一套让人类和AI作为团队成员持续协作的框架。它不是一份 prompt 模板，而是一个完整的团队运行系统——包含身份管理、记忆架构、协作协议和多模型编排。

**核心理念：**

- **身份独立于模型** — AI成员的身份由记忆定义，不绑定特定AI模型
- **AI是团队成员** — 有名字、有分工、有私有空间、有质疑权
- **人类是最终批准者** — AI的自主权是被授予的，可以被收回

## 文档结构

| 文档 | 内容 | 适合谁 |
|------|------|--------|
| [**主文档**](MIXIA-Framework.md) | 完整框架：哲学 + 架构 + 协议 + 编排 + SOP | 所有人 |
| [附录A: 快速开始](appendix-a-quickstart.md) | 目录模板 + boot.md 模板 + 验证清单 | 想立即上手的人 |
| [附录B: Schema](appendix-b-schemas.md) | 卡片/任务/交接的标准数据格式 | 需要结构化实现的人 |
| [附录C: Walkthrough](appendix-c-walkthrough.md) | 一个完整案例：从需求到交付的全链路 | 想理解实际运作的人 |
| [附录D: AI规范](appendix-d-ai-spec.md) | MUST/SHOULD/MAY 格式的可执行规则 | AI系统 |

## 30秒快速开始

```bash
# 1. 创建完整目录结构
mkdir -p persona/core
mkdir -p persona/cards/{axioms,principles,heuristics,patterns}
mkdir -p persona/sessions/$(date +%Y-%m)
mkdir -p persona/proposals
mkdir -p persona/.my-agent/private
mkdir -p persona/indexes

# 2. 写 core/boot.md（定义AI成员的身份）
# 3. 写 core/principles.md（3-5条核心原则）
# 4. 写 core/challenge-core.md（AI应该质疑的场景）

# 5. 把 core/ 下的文件作为AI的初始上下文，开始第一次session
```

> **Windows 用户：** 将 `mkdir -p` 替换为 `mkdir`（PowerShell 自动创建父目录），将 `$(date +%Y-%m)` 替换为当前年月如 `2026-03`。

详见 [附录A](appendix-a-quickstart.md)。

## 适用场景

- 一人团队 + AI：个人开发者用多个AI成员组成虚拟团队
- 小团队 + AI：几个人类成员 + AI成员的混合协作
- 需要跨会话连续性的长期项目
- 需要多个AI模型协作的复杂任务

## 不适用场景

- 一次性问答（不需要身份和记忆）
- 纯聊天/娱乐（不需要协作协议）
- 对AI没有持续协作需求的场景

## License

MIT — 自由使用、修改和分发。

---

**关于署名：** GUAN、Coco、Gemi 是鸣弦团队中AI成员的公开代号（pseudonyms），不关联任何个人身份信息。框架倡导所有使用者同样使用代号而非真实姓名。

*Produced by the MIXIA Collective — GUAN, Coco, Gemi, and our human teammate.*
