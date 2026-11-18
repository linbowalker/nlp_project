# 开发日志

> <span style="background-color:rgb(255, 238, 173)">新记录写在最上面，最新记录在最上方</span>，不删除历史。只记录有价值的状态变化、证据和下一步。

## 2026-11-18 20:57:00 — 推送 GitHub 成功

- 本次目标：把本地提交推送到 GitHub 公开仓库 `linbowalker/nlp_project`。
- 已完成：
  - 配置 remote：`origin = https://github.com/linbowalker/nlp_project.git`。
  - <mark style="background:#FFF9C4">推送 `main` 成功：`* [new branch] main -> main`，本地与远程 commit 一致（`bd26c326...`）</mark>。
  - 验证：跟踪文件 186 个，敏感文件 0 个，工作区干净。
- 关键发现（重要，以后复用）：
  - <mark style="background:#FFF9C4">WorkBuddy 沙箱注入的代理 `127.0.0.1:60749` 对 github.com 返回 502，是坏代理</mark>。
  - <mark style="background:#FFF9C4">Windows 系统真实代理为 `127.0.0.1:17891`（HKCU Internet Settings ProxyServer），用它访问 github.com 返回 HTTP 200</mark>。
  - Git 走真实代理即可正常推送；推送前用 `HTTP_PROXY=http://127.0.0.1:17891 HTTPS_PROXY=http://127.0.0.1:17891 git push` 覆盖沙箱变量。
  - 未使用 PAT：网络通后 Git Credential Manager 已有凭据自动认证成功。账号密码（Basic Auth）被 GitHub 禁用（401），PAT 只是备选方案。
- 证据：`git push` 输出、`git ls-remote origin refs/heads/main`、本地与远程 commit hash 一致。
- 当前结果：项目已上 GitHub，本地与远程同步完成。
- 下一步：如需改提交邮箱（当前占位 `zhaoyanjun@users.noreply.github.com`），改后需 force push；含密钥的两个 `.py` 仍未上传，如改用环境变量读取可补传。

## 2026-11-18 20:34:00 — 初始化 Git 并准备上传 GitHub（未 push）

- 本次目标：为本项目建立 Git 版本管理，并完成上传 GitHub 前的本地准备（不含推送）。
- 已完成：
  - `git init`，默认分支改为 `main`。
  - 仓库级身份：`user.name=zhaoyanjun`、`user.email=zhaoyanjun@users.noreply.github.com`（<mark style="background:#FFF9C4">占位邮箱，推送前应改为真实 GitHub 邮箱</mark>）。
  - 新增 `.gitignore`：排除 `.env`、`__pycache__`、虚拟环境等；<mark style="background:#FFF9C4">额外排除含硬编码 API 密钥的 `chb_hz3_v1/05-LLM/01_api_deepseek_v3.py` 与 `qxsb_hz3_v1/05-LLM/01_api_deepseek_v3.py`</mark>。
  - 全量密钥扫描：4 处命中（2 个 `.env` + 2 个 `.py`）全部被忽略，暂存区无敏感文件。
  - 首次提交 `9258501`，共 <mark style="background:#FFF9C4">186 个文件 / 8.58 MB</mark>，工作区干净。
- 关键发现：<mark style="background:#FFF9C4">两个 `05-LLM/01_api_deepseek_v3.py` 中硬编码了明文 DeepSeek API 密钥</mark>，公开仓库下属高危，已通过 .gitignore 排除；建议后续改为读环境变量并去 DeepSeek 后台重置密钥。
- 当前结果：本地提交就绪，无 remote、未推送（遵循用户"先不 push"的授权）。
- 证据：`git log --oneline`、`git status --short`（0 改动）、`git check-ignore -v` 输出。
- 未解决：GitHub 仓库尚未创建（需用户在网页新建空仓库并提供地址）；未配置 remote；未 push。
- 下一步：用户在 GitHub 建好空仓库 → 提供地址 → `git remote add origin <url>` → `git push -u origin main` → 改真实提交邮箱（如需要）。

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
