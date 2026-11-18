# 项目记忆

> 本文件保存项目的"当前真实状态"。历史过程写入 `DEV_LOG.md`。  
> 不要记录密码、Token、私钥、Cookie 或完整凭据。  
> 最后更新：2026-11-18 20:13:05

## 0. 文档元信息

- 项目名称：<mark style="background:#FFF9C4">NLP项目实战</mark>（`NLP_group04_zhaoyanjun`）
- 项目根目录：`D:\code\NLP_group04_zhaoyanjun`
- 仓库与分支：<span style="background-color:rgb(255, 238, 173)">非 Git 仓库</span>（`git status` 返回 `not a git repository`），无 remote / branch 信息
- 当前负责人：<mark style="background:#FFF9C4">zhaoyanjun</mark>
- 创建时间：2026-11-18 20:13:05
- 最后更新时间：2026-11-18 20:13:05
- 当前阶段：初始化
- 总体状态：🟡 待梳理
- 当前版本或里程碑：M0 项目梳理

## 1. 项目目标

### 1.1 核心目标

- <span style="background-color:rgb(255, 238, 173)">两套并行的中文文本分类课程作业流水线</span>（依据目录结构与 `class.txt`、提示词文件推断，未见正式需求文档）：
  - `chb_hz3_v1`：中文有害/违规内容分类，6 类——黑产广告、欺诈、博彩、不违规、谩骂引战、低俗。
  - `qxsb_hz3_v1`：中文情绪识别分类，8 类——平静、开心、伤心、生气、惊讶、厌恶、疑问、关心。
- 每套均覆盖从数据构建到模型部署的完整链路：`00-dataset` → `01-data` → `02-rf` → `03-fasttext` → `04-bert` → `05-LLM` → `06-bert_distill` → `07-bert_pruning`。

### 1.2 主要交付物

- 两套流水线的 Python 脚本（共 121 个 `.py` 文件）、数据集（`.txt`）、模型压缩/蒸馏/剪枝实验代码。
- 每个模型阶段配 `api_flask_server.py`（Flask API）与 `app_streamlit.py` / `app_streamlit_run.py`（Streamlit 演示）。
- 依赖清单：`reqirements.txt`（GPU 版）、`reqirementscpu.txt`（CPU 版）——注意文件名本身拼写为 `reqirements`，非标准 `requirements`。

### 1.3 非目标与范围边界

- 工作范围（用户负责哪一套 / 哪几个阶段）：**待确认**。
- 需求来源（是否有课程 PPT 或文档）：**待确认**，当前 README.md 为空文件。

### 1.4 验收标准

- 待确认（无需求文档可依据）。

## 2. 关键要求与约束

### 2.1 功能要求

- 文本分类：输入中文文本，输出固定类别标签（chb 6 类 / qxsb 8 类）。
- LLM 阶段要求模型只返回指定类别之一（`大模型生成提示词.txt` 中有明确提示词约束）。

### 2.2 非功能要求

- 性能：待确认
- 兼容性：<span style="background-color:rgb(255, 238, 173)">GPU/CPU 两套依赖分别锁定 torch 版本</span>——GPU 版 `torch==2.9.1+cu128` / `torchvision==0.24.1+cu128`，CPU 版 `torch==2.9.1` / `torchvision==0.24.1`
- 安全性：`.env` 中含 `DEEPSEEK_API_KEY` 等密钥，**不在文档中记录任何值**；只记录变量名。
- 可维护性：待确认
- 交付形式：课程作业（形式待确认）

### 2.3 已确认约束

- <span style="background-color:rgb(255, 238, 173)">所有 `config.py` 中 `root_path` 硬编码为旧机器路径 `F:\workspace\chb_hz3` / `F:\workspace\qxsb_hz3`</span>；本机（D 盘）直接运行会因路径不存在失败，见 `ISSUES.md`。
- 数据集规模：chb 5400/300/300（train/dev/test），qxsb 3743/207/209。

## 3. 当前开发状态

### 3.1 已完成

- [x] 项目记忆初始化（只表示文档框架已创建，不表示项目开发完成）。

### 3.2 进行中

- 当前任务：项目初始化与现状梳理。
- 开始时间：2026-11-18 20:10
- 当前做到：完成自动发现（Git / 构建系统 / 源码结构 / 依赖 / 运行时 / 入口点），已建立 `zyj_docs/` 与项目记忆文件。
- 准确停止位置：初始化文档写入完成，尚未运行任何构建/测试，尚未确认用户工作范围与需求。
- 相关文件：`zyj_docs/project-memory/PROJECT_MEMORY.md`。

### 3.3 下一步（按执行顺序）

1. 确认项目名称、需求来源、工作范围、紧急程度（见 3.5）。
2. 修正两套代码中 `config.py` 的硬编码路径，使其指向当前项目根目录。
3. 选择并验证 Python 运行环境（现有 conda 环境无专用 NLP 环境）。
4. 运行一次数据预处理或模型训练作为可验证的基线与验证状态。

### 3.4 阻塞项

- 当前项目代码中的硬编码路径 `F:\workspace\...` 在本机不可用；未修正前无法直接运行任何阶段脚本。
- 尚无需求文档，无法确认验收标准。

### 3.5 待确认问题

- 是否有课程需求文档 / PPT？路径是什么？
- 你主要负责 `chb`（有害文本）还是 `qxsb`（情绪识别），还是两套都要维护？
- 紧急程度与交付节点？
- 运行环境用本机 Python 3.13，还是需要另建专用 conda 环境？

## 4. 里程碑与关键节点

| 里程碑     | 目标          | 状态  | 计划时间 | 实际时间       | 验收证据                                        |
| ------- | ----------- | --- | ---- | ---------- | ------------------------------------------- |
| M0 项目梳理 | 明确现状、要求和下一步 | 进行中 | 待确认  | 2026-11-18 | `zyj_docs/project-memory/PROJECT_MEMORY.md` |

## 5. 技术与架构摘要

- 技术栈：<span style="background-color:rgb(255, 238, 173)">Python + PyTorch / Transformers（BERT）+ scikit-learn（TF-IDF + 随机森林）+ fastText + jieba + LangChain / LangGraph + DeepSeek-V3 API / Ollama(Qwen) + Flask + Streamlit</span>
- 核心模块：
  - `chb_hz3_v1/`：6 类有害文本分类，`00-dataset`～`07-bert_pruning` 共 8 个阶段。
  - `qxsb_hz3_v1/`：8 类情绪识别，阶段与上相同。
  - 每阶段目录自包含：`config.py` 配置 + 训练/预测脚本 + `api_flask_server.py` + `app_streamlit*.py` + `final_data/` / `result/`。
- 关键数据流：原始 `.txt`（`标签\t文本` 格式）→ 数据清洗/EDA → TF-IDF 或词向量 → 分类模型 → Flask / Streamlit 服务。
- 外部依赖或服务：DeepSeek API（`.env` 中 `BASE_URL`、`DEEPSEEK_API_KEY`）、Ollama 本地模型（`04_ollama_api_qwen.py`）、MySQL（`mysql-connector-python`）。
- 重要接口：各阶段 `api_flask_server.py` 提供 HTTP 推理接口（具体路由待核实）。
- 关键设计说明：详见 `DECISIONS.md`（当前无记录，因未发现已明确的决策）。

## 6. 环境与运行状态

- 开发系统：Windows（win32），Shell：Git Bash。
- 运行环境：<span style="background-color:rgb(255, 238, 173)">本机 `python` 为 Python 3.13.14（conda base），conda 26.5.3，pip 26.1.2，node v22.22.2</span>
- 依赖管理：`reqirements.txt`（GPU）与 `reqirementscpu.txt`（CPU），采用 `==` 精确锁定版本。
- 硬件与资源：待确认（依赖清单含 `torch==2.9.1+cu128`，源项目使用 CUDA 12.8）。
- 环境变量名称：`BASE_URL`、`DEEPSEEK_API_KEY`、`DEV2FILE`、`CLASS_FILE`（**只记录名称，不记录值**）。
- 详细说明：详见 `ENVIRONMENT.md`。

## 7. 验证状态

- 最近构建：未验证
- 最近测试：未验证
- 已知失败：待确认
- 覆盖范围：待确认
- 最近可运行版本：待确认（源机器 `F:\workspace\` 下曾运行，本机未验证）
- 验证证据：待确认

## 8. 重要路径与产物

| 类型       | 路径或名称                                       | 用途             | 状态         |
| -------- | ------------------------------------------- | -------------- | ---------- |
| 项目记忆     | `zyj_docs/project-memory/PROJECT_MEMORY.md` | 当前状态快照         | 已创建        |
| 开发日志     | `zyj_docs/project-memory/DEV_LOG.md`        | 过程历史           | 已创建        |
| 环境记录     | `zyj_docs/project-memory/ENVIRONMENT.md`    | 可复现环境信息        | 已创建        |
| 命令记录     | `zyj_docs/project-memory/COMMANDS.md`       | 已验证命令          | 已创建        |
| 问题记录     | `zyj_docs/project-memory/ISSUES.md`         | 阻塞与风险          | 已创建        |
| 文档索引     | `zyj_docs/README.md`                        | 文档导航           | 已创建        |
| 项目指令     | `AGENTS.md`                                 | 记忆恢复规则         | 已创建        |
| 源码（有害文本） | `chb_hz3_v1/`                               | 6 类有害文本分类流水线   | 已发现        |
| 源码（情绪识别） | `qxsb_hz3_v1/`                              | 8 类情绪识别流水线     | 已发现        |
| 依赖清单     | `reqirements.txt` / `reqirementscpu.txt`    | GPU / CPU 依赖版本 | 已发现        |
| 原始数据     | `*/00-dataset/{train,dev,test}.txt`         | 训练/验证/测试集      | 已发现        |

## 9. 关键决策摘要

- 暂无已明确的决策记录；如需补充详见 `DECISIONS.md`。

## 10. 已知问题、风险与技术债

- 所有 `config.py` 硬编码旧机器路径，见 `ISSUES.md` ISSUE-001。
- 无 Git 版本管理，见 `ISSUES.md` ISSUE-002。
- 依赖文件名拼写异常（`reqirements`），见 `ISSUES.md` ISSUE-003。

## 11. 最近一次工作摘要

- 时间：2026-11-18 20:13:05
- 做了什么：运行 `project-init` skill 完成项目初始化——自动发现项目事实、建立 `zyj_docs/` 文档体系与 `AGENTS.md`、填充项目记忆。
- 结果：记忆框架已建立，项目结构、技术栈、依赖与环境已记录；目标、验收、工作范围等待确认。
- 未完成：硬编码路径修正、运行环境验证、构建/测试基线。

## 12. 重启后恢复指令

复制给新的开发会话或 AI Agent：

> 请先读取 `zyj_docs/project-memory/PROJECT_MEMORY.md` 和 `zyj_docs/project-memory/DEV_LOG.md` 的最新记录，再检查当前仓库状态。用"当前阶段、最近完成、正在进行、下一步、阻塞项、验证状态"六项总结项目现状。不要根据计划推断已完成状态；发生冲突时，以代码、Git、测试、构建和产物证据为准。然后从"下一步"第 1 项继续，并在完成有意义的工作后更新项目记忆。
