# 先安装: pip install openai
# 导包
from dotenv import load_dotenv

load_dotenv()
import os
from openai import OpenAI

api_key = os.getenv("DEEPSEEK_API_KEY")
print("api_key-->", api_key)
base_url = os.getenv("BASE_URL")
print("base_url-->", base_url)

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
   - 低俗（色情、庸俗、不雅内容）

**分类标准：**
- 黑产广告：涉及账号买卖、刷单、非法代发等黑灰产交易推广
- 欺诈：包含诈骗、虚假信息、误导性获利内容
- 博彩：明确提及赌博、赌注、彩票投机等内容
- 不违规：普通日常交流、积极中立或无明显违规特征的内容
- 谩骂引战：含人身攻击、侮辱、挑衅、恶意引战言论
- 低俗：涉及色情暗示、庸俗下流、不雅描述的内容

**输出格式：**
仅返回类别名称，不要添加任何解释、标点或额外文字。

**示例：**
输入："抖音代发加我 70一条"
输出："黑产广告"

输入："今天是一个美好的一天。"
输出："不违规"

输入："他邀请她一起吃午餐。"
输出："不违规"

现在请对以下文本进行分类：
"""


def get_deepseek_res(prompt):
    # 创建客户端
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=os.getenv("BASE_URL"))
    # 创建会话
    response = client.chat.completions.create(
        # 模型deepseek-chat是deepseek-v3
        # 模型deepseek-reasoner是deepseek-r1
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        stream=True
    )
    return response


if __name__ == '__main__':
    # 测试不同的有害文本分类
    test_texts = [
        "抖音代发加我 70一条",
        "他邀请她一起吃午餐。",
        "今天是一个美好的一天。",
        "快速赚钱，稳赚不赔的投资机会！",
        "免费体验在线赌场，注册送彩金！",
        "你这个白痴，根本不配说话！",
        "晚上来我房间，有好东西给你看",
    ]

    for text in test_texts:
        print(f"输入文本: {text}")
        print("分类结果: ", end='')
        res = get_deepseek_res(text)
        for chunk in res:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end='')
        print("\n" + "-" * 50)