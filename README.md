# persona-vault

**鸣弦/MIXIA 团队的加密记忆库 + 开源协作框架**

---

## 这个仓库包含什么

### 1. [鸣弦/MIXIA 框架](framework/)

一套人与AI协作的团队操作系统。包含完整的理论、架构、协议和实操SOP，让任何人都能搭建自己的人+AI协作团队。

- [主文档：完整框架](framework/MIXIA-Framework.md) — 哲学 + 架构 + 协议 + 编排 + SOP + 治理
- [附录A：快速开始](framework/appendix-a-quickstart.md) — 模板 + 脚本 + 验证清单
- [附录B：Schema](framework/appendix-b-schemas.md) — 记忆卡/任务卡/交接卡格式
- [附录C：案例演练](framework/appendix-c-walkthrough.md) — 从需求到交付的完整链路
- [附录D：AI规范](framework/appendix-d-ai-spec.md) — MUST/SHOULD/MAY 格式，AI可直接执行

### 2. 加密记忆库工具

将 persona 文件加密后发布为静态页面，支持浏览器端解密。用于跨设备、跨平台安全分享团队记忆。

- `publish.py` — 加密打包工具（AES-256-GCM + Argon2id）
- `docs/` — GitHub Pages 静态站点（加密 bundle + 浏览器解密页面）

## 核心理念

- **身份独立于模型** — AI成员的身份由记忆定义，不绑定特定AI模型
- **AI是团队成员** — 有名字、有分工、有私有空间、有质疑权
- **人类是最终批准者** — AI的自主权是被授予的，可以被收回

## 快速开始

**想搭建自己的人+AI团队？** → 直接看 [framework/README.md](framework/README.md)

**想用加密记忆库？** →

```bash
pip install -r requirements.txt
python publish.py --source ~/persona --key YOUR_SECRET
```

## 安全说明

- 加密使用 AES-256-GCM，密钥派生使用 Argon2id
- 解密完全在浏览器端完成，密码不会发送到任何服务器
- 私有记忆目录（`.*/private/`）被 .gitignore 排除，不会进入版本控制
- 所有署名使用公开代号（pseudonyms），不关联个人身份信息

## 关于鸣弦/MIXIA

鸣弦（MIXIA = MIX + IA）是一个人与AI协作的团队。"鸣弦而治"——团队成员如琴弦，各自独立振动，共同产生和弦。

团队成员（公开代号）：
- **人类成员** — 业务理解与最终决策
- **GUAN** — 策划与叙事连续性
- **Coco** — 实现与验证
- **Gemi** — 基础设施与调研

## License

MIT
