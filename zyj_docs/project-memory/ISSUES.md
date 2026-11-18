# 问题、阻塞与风险

> 最后更新：2026-11-18 20:13:05
> 只记录会影响后续工作的问题；解决后保留历史并标注证据。

## 状态说明

- `待处理`：尚未开始处理。
- `调查中`：正在定位原因或验证判断。
- `阻塞`：导致当前工作无法继续。
- `已规避`：已有临时方案，但根因尚未解决。
- `已解决`：已经解决并具有验证证据。
- `已延期`：明确不在当前阶段处理。

## 问题清单

### ISSUE-001 — 所有 config.py 硬编码旧机器路径

- 类型：阻塞
- 严重程度：高
- 状态：待处理
- 首次发现：2026-11-18 20:12
- 表现：`chb_hz3_v1/*/config.py` 与 `qxsb_hz3_v1/*/config.py` 中 `root_path` 写死为 `F:\workspace\chb_hz3`、`F:\workspace\qxsb_hz3`。
- 复现与证据：`cat qxsb_hz3_v1/01-data/config.py` → `self.root_path = r'F:\workspace\qxsb_hz3'`；`cat chb_hz3_v1/02-rf/config.py` → `self.root_path = r'F:\workspace\chb_hz3/'`。
- 影响：<mark style="background:#FFF9C4">本项目已迁移到 `D:\code\NLP_group04_zhaoyanjun`，旧路径不存在，所有阶段脚本无法定位数据/模型文件</mark>。
- 当前判断：已验证事实——路径为源码字面量；假设——直接替换为当前项目根路径即可恢复（尚未实测）。
- 临时方案：无（需用户确认后再改代码，见 skill 权限分级）。
- 下一步：向用户确认是否同意批量修正 `config.py` 的 `root_path`。
- 负责人：待确认
- 解决时间：-
- 解决方案与验证：-

### ISSUE-002 — 项目无 Git 版本管理

- 类型：风险
- 严重程度：中
- 状态：待处理
- 首次发现：2026-11-18 20:11
- 表现：`git status` / `git log` 均返回 `fatal: not a git repository`。
- 复现与证据：在项目根目录执行上述命令的输出。
- 影响：无法追踪改动、回滚或协作；项目记忆中的"Git 最新提交"类信息不可用。
- 当前判断：已验证事实——无 `.git` 目录。
- 临时方案：依靠 `zyj_docs/project-memory/` 记录状态。
- 下一步：询问用户是否需要 `git init` 建立版本管理（需确认，不擅自执行）。
- 负责人：待确认
- 解决时间：-
- 解决方案与验证：-

### ISSUE-003 — 依赖清单文件名拼写异常

- 类型：风险
- 严重程度：低
- 状态：待处理
- 首次发现：2026-11-18 20:12
- 表现：依赖文件名为 `reqirements.txt` / `reqirementscpu.txt`（少了一个 `u`），非标准 `requirements*.txt`。
- 复现与证据：`ls` 输出。
- 影响：按常规命令 `pip install -r requirements.txt` 会找不到文件；自动化工具可能不识别。
- 当前判断：已验证事实——文件名确为拼写形式。
- 临时方案：安装时使用准确文件名 `reqirements.txt`。
- 下一步：确认是否重命名为标准名（需用户同意，属代码/文件改动）。
- 负责人：待确认
- 解决时间：-
- 解决方案与验证：-

### ISSUE-004 — Python 与 pip 报告的解释器版本不一致

- 类型：待确认问题
- 严重程度：中
- 状态：调查中
- 首次发现：2026-11-18 20:12
- 表现：`python --version` 输出 3.13.14；`pip --version` 输出 `python 3.14`。
- 复现与证据：见 `ENVIRONMENT.md`「运行时与依赖」表。
- 影响：直接用 pip 安装依赖可能装到与 python 不同的解释器环境。
- 当前判断：已验证事实——两个命令输出的版本号不同；假设——PATH 中 python 与 pip 来自不同位置。
- 临时方案：安装前用 `python -m pip --version` 确认归属。
- 下一步：验证 `which python` 与 `which pip`，决定统一解释器方案。
- 负责人：待确认
- 解决时间：-
- 解决方案与验证：-
