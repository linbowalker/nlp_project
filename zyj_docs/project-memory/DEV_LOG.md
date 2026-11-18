# 开发日志

> <span style="background-color:rgb(255, 238, 173)">新记录写在最上面，最新记录在最上方</span>，不删除历史。只记录有价值的状态变化、证据和下一步。

## 2026-11-18 20:17:52 — 确认项目元信息

- 本次目标：落实用户确认的项目名称与负责人，删除对应的旧"待确认"信息。
- 已完成：
  - 项目名称：<mark style="background:#FFF9C4">NLP项目实战</mark>（替换原推断名"NLP 第4组课程作业"）。
  - 当前负责人：<mark style="background:#FFF9C4">zhaoyanjun</mark>（替换原"待确认"）。
  - 删除 `PROJECT_MEMORY.md` 3.5 节中"项目名称/称呼待确认"条目。
  - 同步更新 `zyj_docs/README.md` 速览表的项目名。
- 当前结果：项目元信息已由用户确认，非推断值。
- 证据：用户在会话中的明确输入"项目名称：NLP项目实战，当前负责人：zhaoyanjun，里面的旧的信息可以删除"。
- 未解决：需求来源、工作范围、紧急程度、运行环境仍待确认。
- 下一步：确认剩余待确认事项 → 修正 config.py 路径 → 验证运行环境。

## 2026-11-18 20:13:05 — 项目初始化（project-init skill）

- 本次目标：为 `D:\code\NLP_group04_zhaoyanjun` 建立可恢复、可交接的项目记忆基础设施。
- 已完成：
  - 创建 `zyj_docs/README.md` 文档索引。
  - 创建 `zyj_docs/project-memory/PROJECT_MEMORY.md`、`DEV_LOG.md`、`ENVIRONMENT.md`、`COMMANDS.md`、`ISSUES.md`、`archive/`。
  - 创建项目根 `AGENTS.md`（项目记忆恢复规则）。
- 当前结果：记忆框架已就绪，关键项目事实已依据只读探查填充。
- 读取的证据（阶段 2 自动发现，全部只读命令）：
  - `git remote -v` / `git branch --show-current` / `git log -5` / `git status --short` → `<mark style="background:#FFF9C4">均返回 `fatal: not a git repository`，确认非 Git 仓库</mark>`。
  - `find . -maxdepth 3` → 两套并行流水线 `chb_hz3_v1/`、`qxsb_hz3_v1/`，各 8 个阶段目录，共 121 个 `.py` 文件、55 个 `.txt`、4 个 `.png`、2 个 `.env`。
  - `reqirements.txt` / `reqirementscpu.txt` → GPU 版含 `torch==2.9.1+cu128`，CPU 版含 `torch==2.9.1`；两文件均精确锁定版本。
  - `01-data/class.txt` → chb：黑产广告/欺诈/博彩/不违规/谩骂引战/低俗；qxsb：平静/开心/伤心/生气/惊讶/厌恶/疑问/关心。
  - `大模型生成提示词.txt` → 确认 chb 为"中文有害文本分类"任务。
  - 各阶段 `config.py` → `<mark style="background:#FFF9C4">硬编码 `root_path = r'F:\workspace\chb_hz3'` / `r'F:\workspace\qxsb_hz3'`</mark>`（见 ISSUE-001）。
  - `.env` → 仅提取变量名 `BASE_URL`、`DEEPSEEK_API_KEY`、`DEV2FILE`、`CLASS_FILE`，<mark style="background:#FFF9C4">未读取、未记录任何值</mark>。
  - `wc -l */00-dataset/{train,dev,test}.txt` → chb 5400/300/300，qxsb 3743/207/209。
  - 运行时：`python 3.13.14`、`conda 26.5.3`、`pip 26.1.2`、`node v22.22.2`；conda envs：base/lerobot/lerobot312/myenv/yolocount（无专用 NLP 环境）。
- 当前结果：项目结构、技术栈、依赖、环境已记录；<mark style="background:#FFF9C4">项目目标/验收/工作范围/需求来源/紧急程度均标"待确认"，未编造</mark>。
- 证据：本目录本次创建的全部记忆文件。
- 未解决：需求文档缺失、硬编码路径、无 Git、运行环境未验证、构建/测试未运行。
- 下一步：确认待确认事项 → 修正 config.py 硬编码路径 → 验证运行环境 → 跑通一次数据预处理作为基线。
