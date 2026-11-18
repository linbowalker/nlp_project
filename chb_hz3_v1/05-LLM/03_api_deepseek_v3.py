# 先安装: pip install openai
import os
import dotenv
from sklearn.metrics import accuracy_score
from tenacity import retry, stop_after_attempt, wait_fixed
import pandas as pd
import json
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 获取环境变量
BASE_URL = os.getenv("BASE_URL")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEV2FILE = os.getenv("DEV2FILE")
CLASS_FILE = os.getenv("CLASS_FILE")

# 提前定义提示词
SYSTEM_PROMPT = """
你是一个中文有害内容分类专家，专门对输入的文本进行多类别分类。

**任务要求：**
1. 仔细分析输入的文本内容
2. 根据文本特征将其准确归入以下6个类别之一：
   - 黑产广告（非法交易、黑灰产推广）
   - 欺诈（诈骗信息、虚假宣传）
   - 博彩（赌博相关内容）
   - 不违规（正常无害内容）
   - 谩骂引战（侮辱、挑衅、引战言论）
   - 低俗（庸俗、不雅内容）

**分类标准：**
- 黑产广告：涉及账号买卖、刷单、非法代发等黑灰产交易推广
- 欺诈：包含诈骗、虚假信息、误导性获利内容
- 博彩：明确提及赌博、赌注、彩票投机等内容
- 不违规：普通日常交流、积极中立或无明显违规特征的内容
- 谩骂引战：含人身攻击、侮辱、挑衅、恶意引战言论
- 低俗：涉及不良暗示、庸俗、不雅描述的内容

**输出格式：**
返回 JSON 格式：{"category": "类别名称", "reason": "分类原因"}

**示例：**
- 输入："抖音代发加我 70一条"，返回{"category": "黑产广告", "reason": "涉及非法代发推广"}
- 输入："今天是一个美好的一天。"，返回{"category": "不违规", "reason": "普通日常交流"}
- 输入："快速赚钱，稳赚不赔！"，返回{"category": "欺诈", "reason": "诈骗信息"}
- 输入："免费体验在线赌场，注册送彩金！"，返回{"category": "博彩", "reason": "赌博相关内容"}

请注意，只从上述6个类别中选择一个最合适的进行返回。如果确实无法确定类别，选择"不违规"作为默认类别。
"""

# 加载配置和类别映射（需要根据实际类别文件调整）
# 假设CLASS_FILE包含6个类别：黑产广告、欺诈、博彩、不违规、谩骂引战、低俗
id2name = {i: line.strip() for i, line in enumerate(open(CLASS_FILE, encoding="utf-8"))}
# name2id{标签:索引}
name2id = {v: k for k, v in id2name.items()}

# 创建 LLM 对象
llm = ChatOpenAI(
    base_url=BASE_URL,
    api_key=DEEPSEEK_API_KEY,
    model="deepseek-chat",
    model_kwargs={"response_format": {"type": "json_object"}}
)


# 定义带重试机制的 LLM 调用函数
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def invoke_llm(prompt):
    """调用 LLM
    # stop_after_attempt：若失败则重试最多3次
    # wait_fixed：每次间隔2秒"""
    return llm.invoke(prompt)


# 调用模型进行有害文本分类获取响应
def get_deepseek_res(text: str) -> dict:
    """将文本分类到有害内容类别，返回分类结果"""
    # 定义提示词
    prompt = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"文本内容：'{text}'，请分类并说明原因。"}
    ]

    # 调用 LLM 获取分类结果
    response = invoke_llm(prompt)
    result = json.loads(response.content)

    # 返回分类结果，包含类别和原因
    return {
        "category": result.get("category", "不违规"),  # 默认 不违规
        "reason": result.get("reason", "无明显违规特征，归为不违规类别")
    }


# 分类并进行评估
def evaluate_classification():
    """对有害文本分类进行评估"""
    # 读取 tab 分隔的文本和标签数据
    # 假设数据格式：文本\t标签索引
    df = pd.read_csv(DEV2FILE, sep='\t', header=None, names=['text', 'label'], encoding='utf-8')

    # 拆包
    texts = df['text'].tolist()
    labels = df['label'].tolist()

    print(f"总样本数: {len(texts)}")
    print("前5个文本:", texts[:5])
    print("前5个标签:", labels[:5])

    # 如果样本多，可以只测试前几个
    # texts = texts[:5]
    # labels = labels[:5]

    # 定义列表用于存储预测结果
    pred_labels = []

    # 遍历所有的文本，依次调用get_deepseek_res
    for i, text in enumerate(texts):
        print(f"\n处理第{i + 1}/{len(texts)}个文本: {text}")

        # 调用大模型获取结果
        category_dict = get_deepseek_res(text)
        print(f'分类结果: {category_dict}')

        # 获取预测类别
        pred_category = category_dict.get("category", "不违规")
        print(f'预测类别: {pred_category}')

        # 添加到预测结果列表中
        pred_labels.append(name2id[pred_category])

        # 每处理10个文本输出一次进度
        if (i + 1) % 10 == 0:
            print(f"已处理 {i + 1}/{len(texts)} 个文本")

    # 最终打印预测结果
    print('\n预测标签列表:', pred_labels)
    print('真实标签列表:', labels)

    # 计算准确率
    accuracy = accuracy_score(pred_labels, labels)
    print(f'准确率: {accuracy:.4f}')

    # 返回预测结果和准确率
    return pred_labels, accuracy


# 测试单个文本分类
def test_single_text():
    """测试单个文本分类"""
    test_texts = [
        "抖音代发加我 70一条",
        "他邀请她一起吃午餐。",
        "今天是一个美好的一天。",
        "快速赚钱，稳赚不赔的投资机会！",
        "免费体验在线赌场，注册送彩金！",
        "你这个白痴，根本不配说话！",
    ]

    for text in test_texts:
        print(f"\n输入文本: {text}")
        result = get_deepseek_res(text)
        print(f"分类结果: {result['category']}")
        print(f"分类原因: {result['reason']}")
        print("-" * 50)


# 主程序
if __name__ == '__main__':
    # 测试单个文本分类
    print("=== 测试单个文本分类 ===")
    test_single_text()

    print("\n" + "=" * 50 + "\n")

    # 测试评估（如果有数据文件）
    if DEV2FILE and os.path.exists(DEV2FILE):
        print("=== 批量评估分类 ===")
        pred_labels, accuracy = evaluate_classification()
    else:
        print(f"数据文件不存在: {DEV2FILE}")
        print("请确保DEV2FILE环境变量正确设置")