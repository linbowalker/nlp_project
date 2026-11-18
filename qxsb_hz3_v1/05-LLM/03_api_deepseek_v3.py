# 先安装: pip install openai scikit-learn pandas langchain-openai tenacity python-dotenv

import os
import json
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any
from tenacity import retry, stop_after_attempt, wait_fixed
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from langchain_openai import ChatOpenAI
import dotenv

# -----------------------
# 配置与常量
# -----------------------

dotenv.load_dotenv()

# 环境变量配置
BASE_URL = os.getenv("BASE_URL")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEV2FILE = Path(os.getenv("DEV2FILE", "dev_data.txt"))
CLASS_FILE = Path(os.getenv("CLASS_FILE", "class_labels.txt"))

# 情感类别（固定顺序）
EMOTION_LABELS = ["平静", "开心", "伤心", "生气", "惊讶", "厌恶", "疑问", "关心"]

# 系统提示词
SYSTEM_PROMPT = """
你是一个中文情感分析专家，专门对输入的文本进行情感分类。

**任务要求：**
1. 仔细分析输入的文本内容
2. 根据文本的情感特征将其准确归入以下8个类别之一：
   - 平静（中性、平和、无明显情绪波动的表达）
   - 开心（喜悦、兴奋、愉快、满足的情感）
   - 伤心（悲伤、难过、失落、沮丧的情感）
   - 生气（愤怒、恼火、不满、愤慨的情感）
   - 惊讶（惊奇、意外、震惊的情感）
   - 厌恶（反感、讨厌、嫌弃、恶心的情感）
   - 疑问（疑惑、好奇、询问、不确定的表达）
   - 关心（担忧、关怀、爱护、牵挂的情感）

**分类标准：**
- 平静：语气平和，无明显情绪倾向的陈述或描述
- 开心：包含积极、愉悦、庆祝、满意的情感表达
- 伤心：体现悲伤、失望、痛苦、难过的情感
- 生气：表达愤怒、指责、抱怨、敌对的情绪
- 惊讶：表示意外、吃惊、震撼的情感反应
- 厌恶：体现反感、讨厌、排斥、恶心的情绪
- 疑问：提出问题、表示疑惑、寻求解答的表达
- 关心：表达担忧、关怀、爱护、牵挂的情感

**特别注意：**
1. "关心"类别的识别要点：
   - 关注他人的健康、安全或福祉
   - 表达担忧、牵挂或体贴
   - 提供帮助或支持的建议
   - 温馨、体贴、爱护的表达
   - 与"平静"的区别：关心有明显的积极情感倾向
   - 与"疑问"的区别：关心以关怀为目的，疑问以获取信息为目的

2. 分类优先级原则：
   - 优先识别明显、强烈的情感表达
   - 当多个情感共存时，选择最突出的一个
   - 对于有疑问但包含关心的内容，如果关怀意图明显，优先选"关心"

**输出格式：**
返回 JSON 格式：{"category": "类别名称", "reason": "分类原因"}

**示例：**
- 输入："今天天气不错，心情很好。"，返回{"category": "开心", "reason": "表达愉悦心情"}
- 输入："我只是陈述一个事实而已。"，返回{"category": "平静", "reason": "中性陈述"}
- 输入："为什么会这样？我真的不明白。"，返回{"category": "疑问", "reason": "表示疑惑"}
- 输入："听到这个消息我太难过了。"，返回{"category": "伤心", "reason": "表达悲伤情感"}
- 输入："这简直太让人生气了！"，返回{"category": "生气", "reason": "表达愤怒情绪"}
- 输入："哇！这完全出乎我的意料！"，返回{"category": "惊讶", "reason": "表示意外震惊"}
- 输入："这种行为真让人反感。"，返回{"category": "厌恶", "reason": "表达反感情绪"}
- 输入："最近天气转凉，记得多穿衣服，别感冒了。"，返回{"category": "关心", "reason": "表达关怀体贴"}

请注意，只从上述8个类别中选择一个最合适的进行返回。如果确实无法确定类别，选择"平静"作为默认类别。
"""


# -----------------------
# 实用函数
# -----------------------

def ensure_class_labels_file() -> List[str]:
    """确保类别文件存在，若不存在则创建，并返回标签列表"""
    if not CLASS_FILE.exists():
        print(f"类别文件 {CLASS_FILE} 不存在，正在创建...")
        with open(CLASS_FILE, 'w', encoding='utf-8') as f:
            for label in EMOTION_LABELS:
                f.write(label + '\n')
        print(f"✅ 已创建 {CLASS_FILE}")
    else:
        print(f"✅ 使用现有类别文件: {CLASS_FILE}")

    with open(CLASS_FILE, encoding='utf-8') as f:
        labels = [line.strip() for line in f if line.strip()]
    return labels


def load_label_mappings(labels: List[str]) -> Tuple[Dict[int, str], Dict[str, int]]:
    """构建 id ⇄ label 映射"""
    id2name = {i: label for i, label in enumerate(labels)}
    name2id = {label: i for i, label in enumerate(labels)}
    return id2name, name2id


def create_example_data_file():
    """创建示例数据文件（tsv格式：text \t label_id）"""
    example_data = [
        ("今天阳光明媚，心情特别愉快！", 1),  # 开心
        ("实验结果符合预期，数据正常。", 0),  # 平静
        ("我的钱包不见了，里面有所有证件。", 2),  # 伤心
        ("你怎么能这样对我说话！", 3),  # 生气
        ("天啊！我完全没想到会是这个结果！", 4),  # 惊讶
        ("这种味道真的让我受不了。", 5),  # 厌恶
        ("为什么这个问题一直解决不了？", 6),  # 疑问
        ("最近降温了，出门记得加件外套，别着凉了。", 7),  # 关心
        ("周末和朋友一起看了场电影。", 0),  # 平静
        ("终于完成了这个项目，太有成就感了！", 1),  # 开心
        ("听到这个消息，我的心都碎了。", 2),  # 伤心
        ("我受够了这种不公平的待遇！", 3),  # 生气
        ("什么？这怎么可能发生？", 4),  # 惊讶
        ("看到这种场面让我觉得很不舒服。", 5),  # 厌恶
        ("你脸色不太好，是不是哪里不舒服？需要去医院吗？", 7),  # 关心
        ("这个方案具体是怎么实施的？", 6),  # 疑问
        ("别太拼了，身体是革命的本钱。", 7),  # 关心
        ("工作再忙也要按时吃饭，胃不好更要注意。", 7),  # 关心
        ("这个问题我们需要进一步研究。", 0),  # 平静
        ("太棒了！我们终于成功了！", 1),  # 开心
    ]

    with open(DEV2FILE, 'w', encoding='utf-8') as f:
        for text, label in example_data:
            f.write(f"{text}\t{label}\n")
    print(f"✅ 已创建示例数据文件: {DEV2FILE}（{len(example_data)} 条）")


def init_llm() -> ChatOpenAI:
    """初始化 LLM 客户端"""
    if not BASE_URL or not DEEPSEEK_API_KEY:
        raise ValueError("请在 .env 文件中设置 BASE_URL 和 DEEPSEEK_API_KEY")

    return ChatOpenAI(
        base_url=BASE_URL,
        api_key=DEEPSEEK_API_KEY,
        model="deepseek-chat",
        model_kwargs={"response_format": {"type": "json_object"}},
        temperature=0.1,
        max_tokens=100,
    )


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def invoke_llm(llm: ChatOpenAI, messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """带重试的 LLM 调用，返回解析后的 dict"""
    response = llm.invoke(messages)
    try:
        result = json.loads(response.content)
        return result
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM 返回非 JSON 内容: {response.content[:100]}...") from e


def classify_emotion(llm: ChatOpenAI, text: str, valid_labels: set, default_label: str = "平静") -> Dict[str, str]:
    """对单条文本进行情感分类"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"文本内容：'{text}'，请进行情感分类并说明原因。"}
    ]

    try:
        result = invoke_llm(llm, messages)
        category = result.get("category", default_label)
        reason = result.get("reason", "无明确原因")

        if category not in valid_labels:
            logging.warning(f"模型返回无效类别 '{category}'，回退为 '{default_label}'")
            category = default_label
            reason = f"原类别 '{category}' 无效，已回退"

        return {"category": category, "reason": reason}

    except Exception as e:
        logging.error(f"分类失败（文本：{text[:30]}...）: {e}")
        return {"category": default_label, "reason": f"分类失败: {str(e)}"}


def evaluate_on_dataset(llm: ChatOpenAI, id2name: Dict[int, str], name2id: Dict[str, int]) -> Tuple[List[int], float]:
    """在数据集上进行批量评估"""
    if not DEV2FILE.exists():
        print(f"⚠️ 数据文件 {DEV2FILE} 不存在，正在生成示例数据...")
        # create_example_data()

    try:
        df = pd.read_csv(DEV2FILE, sep='\t', header=None, names=['text', 'label'], encoding='utf-8')
    except Exception as e:
        raise RuntimeError(f"无法读取数据文件 {DEV2FILE}: {e}")

    texts = df['text'].tolist()
    true_labels = df['label'].astype(int).tolist()

    print(f"📊 总样本数: {len(texts)}")
    print("前3个样本:", list(zip(texts[:3], [id2name.get(l, '未知') for l in true_labels[:3]])))

    valid_labels = set(name2id.keys())
    pred_labels = []
    default_label = "平静"

    for i, text in enumerate(texts):
        print(f"\r[{i+1}/{len(texts)}] 处理中...", end='', flush=True)
        res = classify_emotion(llm, text, valid_labels, default_label)
        pred_id = name2id.get(res['category'], 0)
        pred_labels.append(pred_id)

    print("\n✅ 分类完成！")

    # 计算指标
    accuracy = accuracy_score(true_labels, pred_labels)
    target_names = [id2name[i] for i in sorted(id2name.keys())]

    print(f"\n{'='*60}")
    print(f"准确率: {accuracy:.4f}")
    print(f"{'='*60}")
    print("\n📋 分类报告:")
    print(classification_report(true_labels, pred_labels, target_names=target_names))
    print("\n🧮 混淆矩阵:")
    cm_df = pd.DataFrame(
        confusion_matrix(true_labels, pred_labels),
        index=target_names,
        columns=target_names
    )
    print(cm_df)

    return pred_labels, accuracy


def test_single_texts(llm: ChatOpenAI, valid_labels: set):
    """测试单条文本分类"""
    test_cases = [
        "今天阳光明媚，心情特别愉快！",
        "实验结果符合预期，数据正常。",
        "我的钱包不见了，里面有所有证件。",
        "你怎么能这样对我说话！",
        "天啊！我完全没想到会是这个结果！",
        "这种味道真的让我受不了。",
        "为什么这个问题一直解决不了？",
        "最近降温了，出门记得加件外套，别着凉了。",
        "别太拼了，身体是革命的本钱。",
        "这个结果让人非常失望。"
    ]

    print("\n" + "="*60)
    print("🧪 单条文本情感分类测试")
    print("="*60)

    for i, text in enumerate(test_cases, 1):
        res = classify_emotion(llm, text, valid_labels)
        print(f"\n[{i}] 输入: {text}")
        print(f"    分类: {res['category']}")
        print(f"    原因: {res['reason']}")
        print("-" * 50)


def main():
    logging.basicConfig(level=logging.WARNING)

    # 1. 初始化类别映射
    labels = ensure_class_labels_file()
    if labels != EMOTION_LABELS:
        print("⚠️ 警告：class_labels.txt 中的顺序与代码定义不一致，可能影响 label 映射！")

    id2name, name2id = load_label_mappings(labels)
    print("\n🏷️ 类别映射:")
    for i, name in id2name.items():
        print(f"  {i}: {name}")

    # 2. 初始化 LLM
    llm = init_llm()
    valid_labels = set(name2id.keys())

    # 3. 单条测试
    print("\n=== 🔍 单条测试 ===")
    test_single_texts(llm, valid_labels)

    # 4. 批量评估
    print("\n=== 📈 批量评估 ===")
    evaluate_on_dataset(llm, id2name, name2id)

    print("\n✅ 情感分类系统运行完成！")


if __name__ == '__main__':
    main()