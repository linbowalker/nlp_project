# 常用命令

> 只记录已验证命令。未验证命令必须明确标记，不要写入秘密值。
> 最后更新：2026-11-18 20:13:05

## 初始化探查（已验证，只读）

### 运行时版本

- 用途：记录本机运行时版本
- 工作目录：任意
- 平台或 Shell：Git Bash (Windows)
- 状态：<mark style="background:#FFF9C4">已验证（2026-11-18）</mark>

```bash
python --version      # 3.13.14
conda --version       # 26.5.3
conda env list        # base / lerobot / lerobot312 / myenv / yolocount
pip --version         # pip 26.1.2 (python 3.14)
node --version        # v22.22.2
```

- 预期结果：输出各运行时版本
- 常见错误与处理：conda 在 Git Bash 可能未初始化；本次可用，无需额外配置

### 项目事实探查

- 用途：收集项目结构、依赖、类别、数据规模
- 工作目录：`D:\code\NLP_group04_zhaoyanjun`
- 状态：<mark style="background:#FFF9C4">已验证（2026-11-18）</mark>

```bash
find . -maxdepth 3 -not -path '*/.git/*' | head -300
wc -l chb_hz3_v1/00-dataset/{train,dev,test}.txt qxsb_hz3_v1/00-dataset/{train,dev,test}.txt
sed -n 's/^\([A-Za-z_][A-Za-z0-9_]*\)=.*/\1=<value hidden>/p' chb_hz3_v1/05-LLM/.env   # 只取变量名
```

- 预期结果：目录树、样本行数、 masked 的变量名
- 常见错误与处理：本项目非 Git 仓库，任何 `git` 探查命令都会返回 `fatal: not a git repository`

## 初始化与安装

- 待补充（依赖尚未安装，需先确认运行环境）

```bash
# 未验证，勿直接执行：
# pip install -r reqirementscpu.txt   # CPU 版
# pip install -r reqirements.txt      # GPU 版（需 CUDA 12.8）
```

- 状态：未验证
- 前置条件：确认使用哪个 Python 解释器、GPU/CPU 二选一

## 启动与运行

- 待补充（源路径 `F:\workspace\...` 未修正前，各阶段脚本无法运行）

## 测试与验证

- 待补充

## 构建、打包与发布

- 待补充

## 诊断与恢复

- 待补充
