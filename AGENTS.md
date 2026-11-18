## 项目记忆规则

本项目中，用户自行编写的文档放在 `zyj_docs/` 中；由 Agent 维护的项目状态记忆只能放在专用目录 `zyj_docs/project-memory/` 中。

### 语言规则

1. Agent 创建或维护的项目记忆说明文字默认使用简体中文。
2. 文件名、目录名、命令、参数、环境变量、代码标识、依赖名和必要技术术语保留原文。

### 文档隔离原则

1. 不得修改、移动、重命名、删除或重新整理 `zyj_docs/project-memory/` 之外的任何文件，除非用户明确要求。
2. 不得把项目记忆文件直接创建在 `zyj_docs/` 根目录。
3. `zyj_docs/` 中已有的需求、计划、分析、说明、TODO、README 等均视为用户文档，可以读取参考，但不能擅自改写。

### 开始或恢复开发前

1. 先读取 `zyj_docs/project-memory/PROJECT_MEMORY.md`。
2. 再读取 `zyj_docs/project-memory/DEV_LOG.md` 的最新记录。
3. 按需读取 `ISSUES.md`、`DECISIONS.md`、`ENVIRONMENT.md`、`COMMANDS.md` 和 `RELEASES.md`。
4. 可以读取 `zyj_docs/` 中其他用户文档来核实需求和计划，但不得自动修改。
5. 对照 Git、代码、配置、测试、构建和产物核实记忆；发生冲突时，以可验证项目证据为准，并且只修正 `zyj_docs/project-memory/` 内的记忆文件。
6. 开始工作前，用"当前阶段、最近完成、正在进行、下一步、阻塞项、验证状态"六项概括项目现状。

### 完成有意义的开发工作后

1. 向 `zyj_docs/project-memory/DEV_LOG.md` <mark style="background:#FFF9C4">最上方</mark>追加记录（最新记录在最上面）。
2. 更新 `PROJECT_MEMORY.md` 中的当前阶段、已完成、进行中、下一步、阻塞项和验证状态。
3. 只有对应状态发生变化时，才更新 `DECISIONS.md`、`ISSUES.md`、`ENVIRONMENT.md`、`COMMANDS.md` 或 `RELEASES.md`。
4. 不得在文档中保存密码、Token、私钥、Cookie 或完整凭据。
5. 不得把"计划做"误写成"已完成"；完成状态必须有代码、文件、Git 提交、命令输出、测试、构建、产物或用户确认作为证据。
6. 在结束会话前，必须写清当前任务准确停止位置和按顺序执行的下一步三项动作。
