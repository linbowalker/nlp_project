# 环境记录

> 记录可复现信息，不记录任何秘密值。
> 最后更新：2026-11-18 20:13:05

## 开发环境

- 操作系统：Windows（win32），用户目录 `C:\Users\ASUS`
- Shell：Git Bash
- IDE 或 Agent：WorkBuddy
- CPU、GPU 与内存：待确认（依赖清单含 CUDA 12.8 版本的 torch，源机器应有 NVIDIA GPU）
- 网络与代理要求：待确认（LLM 阶段需访问 DeepSeek API / Ollama 本地服务）

## 运行时与依赖

| 名称 | 版本 | 来源或安装方式 | 用途 | 最后验证 |
|---|---|---|---|---|
| Python（当前 shell） | 3.13.14 | conda base `D:\soft\anaconda3` | 默认解释器 | 2026-11-18 `python --version` |
| conda | 26.5.3 | 已安装 | 环境管理 | 2026-11-18 |
| pip | 26.1.2（python 3.14 环境） | `D:\soft\anaconda3\Lib\site-packages\pip` | 包管理 | 2026-11-18 |
| Node.js | v22.22.2 | 已安装 | 前端/工具链（本项目非必需） | 2026-11-18 |
| torch（GPU 清单） | 2.9.1+cu128 | `reqirements.txt` | 深度学习框架 | 清单记录，未安装验证 |
| torch（CPU 清单） | 2.9.1 | `reqirementscpu.txt` | 深度学习框架 | 清单记录，未安装验证 |
| transformers | 4.57.3 | `reqirements*.txt` | BERT 模型 | 清单记录，未安装验证 |
| scikit-learn | 1.7.2 | `reqirements*.txt` | TF-IDF + 随机森林 | 清单记录，未安装验证 |
| fasttext-wheel | 0.9.2 | `reqirements*.txt` | fastText 分类 | 清单记录，未安装验证 |
| langchain | 1.1.2 | `reqirements*.txt` | LLM 编排 | 清单记录，未安装验证 |
| streamlit | 1.52.1 | `reqirements*.txt` | 演示应用 | 清单记录，未安装验证 |
| Flask | 3.1.2 | `reqirements*.txt` | API 服务 | 清单记录，未安装验证 |

### 已有 conda 环境

| 环境名 | 路径 | 备注 |
|---|---|---|
| base | `D:\soft\anaconda3` | 当前激活 |
| lerobot | `D:\soft\anaconda3\envs\lerobot` | 与本项目的 NLP 栈无直接关系 |
| lerobot312 | `D:\soft\anaconda3\envs\lerobot312` | 同上 |
| myenv | `D:\soft\anaconda3\envs\myenv` | 用途待确认 |
| yolocount | `D:\soft\anaconda3\envs\yolocount` | 同上 |

- <mark style="background:#FFF9C4">尚未发现专用的 NLP/课程 conda 环境</mark>；是否新建环境待用户确认。

## 外部服务

| 服务 | 地址类型 | 用途 | 凭据名称 | 状态 |
|---|---|---|---|---|
| DeepSeek API | 远程（`.env` 中 `BASE_URL`） | LLM 文本分类（`05-LLM`） | `DEEPSEEK_API_KEY` | 未验证 |
| Ollama 本地服务 | 本地 | 本地大模型调用（`04_ollama_api_qwen.py`） | 无（本地） | 未验证 |
| MySQL | 本地/远程，待确认 | 依赖 `mysql-connector-python`，用途待确认 | 待确认 | 未验证 |

## 关键环境变量

| 变量名 | 用途 | 是否必需 | 值的保存位置 |
|---|---|---|---|
| `BASE_URL` | LLM API 地址 | 是（LLM 阶段） | `05-LLM/.env`（值不记录） |
| `DEEPSEEK_API_KEY` | LLM API 密钥 | 是（LLM 阶段） | `05-LLM/.env`（值不记录） |
| `DEV2FILE` | 待确认 | 待确认 | `05-LLM/.env`（值不记录） |
| `CLASS_FILE` | 待确认 | 待确认 | `05-LLM/.env`（值不记录） |

## 环境差异与常见陷阱

- 源项目代码中的 `root_path = r'F:\workspace\...'` 是旧机器路径，在本机必须改为 `D:\code\NLP_group04_zhaoyanjun\...` 或改为相对路径，否则所有阶段脚本无法定位数据。
- `reqirements.txt` 文件名为拼写错误形式，安装时需写全 `reqirements.txt`（不是 `requirements.txt`）。
- GPU/CPU 两份依赖只有 torch/torchvision 版本不同，按硬件二选一，不要混装。
- 当前 shell 的 `python` 为 3.13，而 `pip` 报告 python 3.14，二者可能不在同一环境；实际安装前需确认解释器与 pip 匹配。
