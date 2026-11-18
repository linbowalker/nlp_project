# 项目文档索引（zyj_docs）

> 最后更新：2026-11-18 20:13:05
> 本项目由 `project-init` skill 初始化。文档分层约定：用户自行编写的文档放 `zyj_docs/`，Agent 维护的项目状态记忆放 `zyj_docs/project-memory/`。

## 项目速览

| 项 | 内容 |
|---|---|
| 项目 | <mark style="background:#FFF9C4">NLP项目实战</mark>（`NLP_group04_zhaoyanjun`） |
| 根目录 | `D:\code\NLP_group04_zhaoyanjun` |
| 版本管理 | 非 Git 仓库 |
| 主线 | `chb_hz3_v1`（6 类有害文本分类）、`qxsb_hz3_v1`（8 类情绪识别） |
| 阶段 | 数据 → RF → fastText → BERT → LLM → BERT 蒸馏 → BERT 剪枝 |
| 当前状态 | 🟡 初始化完成，待梳理需求与工作范围 |

## 文档结构

```
zyj_docs/
├── README.md                          ← 本文件，文档索引
└── project-memory/
    ├── PROJECT_MEMORY.md              ← 当前状态快照（新会话先读）
    ├── DEV_LOG.md                     ← 开发日志（最新在最上）
    ├── ENVIRONMENT.md                 ← 环境信息（不含密钥值）
    ├── COMMANDS.md                    ← 已验证命令
    ├── ISSUES.md                      ← 问题、阻塞与风险
    ├── DECISIONS.md                   ← 关键决策（按需创建，当前未建）
    └── archive/                       ← 里程碑归档
```

## 使用方式

1. 新会话 / 重启开发前：先读 `project-memory/PROJECT_MEMORY.md`，再读 `project-memory/DEV_LOG.md` 最新记录，按需读其他记忆文件。
2. 项目根 `AGENTS.md` 已写入相同的恢复规则，Agent 会自动遵循。
3. 完成有意义的工作后：在 `DEV_LOG.md` 最上方追加记录，并更新 `PROJECT_MEMORY.md` 的当前状态。
4. 不要在记忆文件中记录密码、Token 或任何凭据值。

## 待补充文档

- `000_YYYY-MM-DD_需求对照表_持续维护.md`：需用户提供需求文档后创建。
- `DECISIONS.md`：出现明确的关键决策时创建。
