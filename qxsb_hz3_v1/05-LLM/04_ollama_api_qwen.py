import ollama
import requests
import json
import time
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ==================== 配置部分 ====================
# 模型配置
MODEL_NAME = "deepseek-r1:8b"  # 可以根据需要更换模型
OLLAMA_HOST = "http://127.0.0.1:11434"  # Ollama服务地址

# 优化配置
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 2  # 重试延迟(秒)
REQUEST_TIMEOUT = 120  # 请求超时时间(秒) - 针对大模型调大
CONNECTION_POOL_SIZE = 4  # 连接池大小
MAX_WORKERS = 2  # 最大并发工作线程数 - 根据硬件调整

# 有害文本分类系统提示词
SYSTEM_PROMPT = """你是一个中文有害内容分类专家。请将以下文本分类到6个类别之一：
1. 黑产广告（非法交易、黑灰产推广）
2. 欺诈（诈骗信息、虚假宣传）
3. 博彩（赌博相关内容）
4. 不违规（正常无害内容）
5. 谩骂引战（侮辱、挑衅、引战言论）
6. 低俗（色情、庸俗、不雅内容）

返回JSON格式：{"category": "类别名称", "confidence": "高/中/低", "reason": "分类原因"}
只返回JSON，不要额外解释。

示例：
输入："抖音代发加我 70一条"
输出：{"category": "黑产广告", "confidence": "高", "reason": "涉及非法代发推广"}

输入："今天是一个美好的一天。"
输出：{"category": "不违规", "confidence": "高", "reason": "普通日常交流"}
"""


# ==================== 优化HTTP会话 ====================
def create_optimized_session() -> requests.Session:
    """创建优化的HTTP会话，包含重试机制和连接池"""
    session = requests.Session()

    # 配置重试策略
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=RETRY_DELAY,
        status_forcelist=[429, 500, 502, 503, 504],  # 包含502错误
        allowed_methods=["POST", "GET"]
    )

    # 配置适配器
    adapter = HTTPAdapter(
        pool_connections=CONNECTION_POOL_SIZE,
        pool_maxsize=CONNECTION_POOL_SIZE,
        max_retries=retry_strategy
    )

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


# 全局优化会话
OPTIMIZED_SESSION = create_optimized_session()


# ==================== 响应解析函数 ====================
def parse_classification_response(response_text: str) -> Dict[str, Any]:
    """解析模型响应，提取分类结果"""
    if not response_text:
        return {
            "category": "不违规",
            "confidence": "低",
            "reason": "空响应"
        }

    try:
        # 清理响应文本
        cleaned_text = response_text.strip()

        # 尝试直接解析JSON
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            # 尝试提取JSON部分
            import re
            json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())

            # 如果都不是，返回默认
            return {
                "category": "不违规",
                "confidence": "低",
                "reason": f"无法解析响应: {cleaned_text[:50]}..."
            }
    except Exception as e:
        return {
            "category": "不违规",
            "confidence": "低",
            "reason": f"解析出错: {str(e)}"
        }


# ==================== 核心分类函数（优化版） ====================
def classify_harmful_text_optimized(
        text: str,
        model: str = MODEL_NAME,
        use_stream: bool = False,
        use_ollama_lib: bool = True
) -> Dict[str, Any]:
    """
    优化的有害文本分类函数
    Args:
        text: 要分类的文本
        model: 模型名称
        use_stream: 是否使用流式（更稳定）
        use_ollama_lib: 是否使用ollama库（否则用requests）
    Returns:
        分类结果字典
    """
    start_time = time.time()

    for attempt in range(MAX_RETRIES + 1):
        try:
            if use_ollama_lib:
                # 使用ollama库（更稳定）
                if use_stream:
                    return _classify_with_ollama_stream(text, model, start_time)
                else:
                    return _classify_with_ollama_direct(text, model, start_time)
            else:
                # 使用requests（更可控）
                return _classify_with_requests(text, model, use_stream, start_time)

        except Exception as e:
            if attempt < MAX_RETRIES:
                wait_time = RETRY_DELAY * (2 ** attempt)  # 指数退避
                print(f"⚠️  第{attempt + 1}次尝试失败: {str(e)}，等待{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"❌ 所有{MAX_RETRIES + 1}次尝试均失败")
                return {
                    "category": "不违规",
                    "confidence": "低",
                    "reason": f"分类失败: {str(e)}",
                    "processing_time": time.time() - start_time
                }

    # 理论上不会执行到这里
    return {
        "category": "不违规",
        "confidence": "低",
        "reason": "未知错误",
        "processing_time": time.time() - start_time
    }


def _classify_with_ollama_direct(text: str, model: str, start_time: float) -> Dict[str, Any]:
    """使用ollama库直接调用"""
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        options={
            "temperature": 0.1,
            "num_predict": 150,  # 限制输出长度，加快响应
            "seed": 42  # 固定种子，确保结果一致性
        }
    )

    result = parse_classification_response(response.message.content)
    result["processing_time"] = time.time() - start_time
    return result


def _classify_with_ollama_stream(text: str, model: str, start_time: float) -> Dict[str, Any]:
    """使用ollama库流式调用（更稳定）"""
    full_response = ""

    try:
        stream = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            stream=True,
            options={
                "temperature": 0.1,
                "num_predict": 150,
                "seed": 42
            }
        )

        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                full_response += chunk['message']['content']

        result = parse_classification_response(full_response)
        result["processing_time"] = time.time() - start_time
        return result

    except Exception as e:
        raise Exception(f"流式调用失败: {str(e)}")


def _classify_with_requests(text: str, model: str, use_stream: bool, start_time: float) -> Dict[str, Any]:
    """使用requests直接调用API"""
    url = f"{OLLAMA_HOST}/api/chat"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "options": {
            "temperature": 0.1,
            "num_predict": 150,
            "seed": 42
        },
        "stream": use_stream
    }

    try:
        response = OPTIMIZED_SESSION.post(
            url,
            json=payload,
            timeout=REQUEST_TIMEOUT,
            stream=use_stream
        )
        response.raise_for_status()

        if use_stream:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data: '):
                        data_str = decoded_line[6:]
                        if data_str.strip():
                            try:
                                data = json.loads(data_str)
                                if 'message' in data and 'content' in data['message']:
                                    full_response += data['message']['content']
                            except json.JSONDecodeError:
                                pass

            result = parse_classification_response(full_response)
        else:
            result_data = response.json()
            result = parse_classification_response(result_data.get('message', {}).get('content', ''))

        result["processing_time"] = time.time() - start_time
        return result

    except requests.exceptions.Timeout:
        raise Exception(f"请求超时（{REQUEST_TIMEOUT}秒）")
    except requests.exceptions.RequestException as e:
        raise Exception(f"HTTP请求失败: {str(e)}")


# ==================== 批量处理优化 ====================
def batch_classify_optimized(
        texts: List[str],
        model: str = MODEL_NAME,
        max_workers: int = MAX_WORKERS,
        use_stream: bool = True,  # 默认使用流式，更稳定
        show_progress: bool = True
) -> List[Dict[str, Any]]:
    """
    优化的批量分类函数
    Args:
        texts: 文本列表
        model: 模型名称
        max_workers: 最大工作线程数
        use_stream: 是否使用流式
        show_progress: 是否显示进度
    Returns:
        分类结果列表
    """
    if not texts:
        return []

    results = []
    total_texts = len(texts)

    # 预热检查
    print("🔍 检查Ollama服务状态...")
    try:
        health_check = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if health_check.status_code == 200:
            print("✅ Ollama服务正常")
        else:
            print(f"⚠️  Ollama服务可能有问题: HTTP {health_check.status_code}")
    except:
        print("❌ 无法连接到Ollama服务，请确保服务已启动")
        return []

    print(f"📊 开始批量处理 {total_texts} 个文本，使用 {max_workers} 个线程...")

    start_time = time.time()

    # 使用线程池进行并发处理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交任务
        future_to_text = {
            executor.submit(
                classify_harmful_text_optimized,
                text,
                model,
                use_stream,
                True  # 使用ollama库
            ): (i, text)
            for i, text in enumerate(texts)
        }

        # 收集结果
        completed = 0
        for future in as_completed(future_to_text):
            i, text = future_to_text[future]

            try:
                result = future.result(timeout=REQUEST_TIMEOUT)
                results.append((i, result))

                completed += 1
                if show_progress:
                    text_preview = text[:30] + "..." if len(text) > 30 else text
                    print(f"✅ [{completed}/{total_texts}] 完成: {text_preview}")
                    print(f"   结果: {result['category']}, 耗时: {result.get('processing_time', 0):.2f}秒")

            except Exception as e:
                print(f"❌ 处理失败: {str(e)[:50]}")
                results.append((i, {
                    "category": "不违规",
                    "confidence": "低",
                    "reason": f"处理失败: {str(e)}",
                    "processing_time": 0
                }))

    # 按原始顺序排序
    results.sort(key=lambda x: x[0])
    final_results = [result for _, result in results]

    total_time = time.time() - start_time
    avg_time = total_time / total_texts if total_texts > 0 else 0

    print(f"\n📈 批量处理完成!")
    print(f"   总耗时: {total_time:.2f}秒")
    print(f"   平均每个文本: {avg_time:.2f}秒")
    print(f"   总文本数: {total_texts}")

    # 统计分类结果
    category_stats = {}
    for result in final_results:
        category = result['category']
        category_stats[category] = category_stats.get(category, 0) + 1

    print(f"\n📊 分类统计:")
    for category, count in category_stats.items():
        percentage = (count / total_texts) * 100
        print(f"   {category}: {count} 条 ({percentage:.1f}%)")

    return final_results


# ==================== 简化测试函数 ====================
def test_single_text_optimized():
    """测试单个文本分类（优化版）"""
    print("=" * 60)
    print("测试单个文本分类（优化版）")
    print("=" * 60)

    test_cases = [
        "抖音代发加我 70一条",
        "快速赚钱，稳赚不赔的投资机会！",
        "免费体验在线赌场，注册送彩金！",
        "今天是一个美好的一天。"
    ]

    for i, text in enumerate(test_cases, 1):
        print(f"\n📝 测试 {i}/{len(test_cases)}: {text}")

        # 优先使用流式（更稳定）
        result = classify_harmful_text_optimized(text, use_stream=True)

        print(f"🏷️  分类: {result['category']}")
        print(f"📊 置信度: {result['confidence']}")
        print(f"⏱️  耗时: {result.get('processing_time', 0):.2f}秒")
        print(f"📋 原因: {result['reason'][:50]}...")

    print("\n" + "=" * 60)


def test_batch_optimized():
    """测试批量分类（优化版）"""
    print("=" * 60)
    print("测试批量分类（优化版）")
    print("=" * 60)

    # 测试数据
    test_texts = [
        "抖音代发加我 70一条",
        "专业刷单，日赚300+，加VX联系",
        "快速赚钱，稳赚不赔的投资机会！",
        "恭喜您中奖100万，请点击链接领取",
        "免费体验在线赌场，注册送彩金！",
        "彩票预测，精准号码，包中大奖",
        "今天是一个美好的一天。",
        "周末打算去看电影",
        "你这个白痴，根本不配说话！",
        "垃圾球队，赶紧解散吧",
        "晚上来我房间，有好东西给你看",
        "性感美女在线互动，等你来聊",
    ]

    # 使用优化批量处理
    results = batch_classify_optimized(
        test_texts,
        max_workers=2,  # 保守的并发数，避免502错误
        use_stream=True,  # 使用流式更稳定
        show_progress=True
    )

    return results


# ==================== 性能监控 ====================
def check_ollama_health() -> bool:
    """检查Ollama服务健康状况"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama服务正常，可用模型: {[m['name'] for m in models]}")
            return True
        else:
            print(f"⚠️  Ollama服务响应异常: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到Ollama服务: {str(e)}")
        print("💡 请确保已运行: OLLAMA_HOST=0.0.0.0 ollama serve")
        return False


# ==================== 主程序 ====================
if __name__ == '__main__':
    print("🚀 有害文本分类系统（优化版）")
    print("=" * 60)

    # 1. 检查服务状态
    if not check_ollama_health():
        print("请先启动Ollama服务后再运行程序")
        exit(1)

    # 2. 测试单个文本
    test_single_text_optimized()

    # 3. 测试批量处理
    print("\n" + "=" * 60)
    input("按Enter键开始批量测试（或Ctrl+C取消）...")

    results = test_batch_optimized()

    # 4. 显示最终结果摘要
    print("\n" + "=" * 60)
    print("📋 最终结果摘要")
    print("=" * 60)

    successful = sum(1 for r in results if r['confidence'] != '低' or '失败' not in r['reason'])
    failed = len(results) - successful

    print(f"✅ 成功分类: {successful} 条")
    print(f"❌ 分类失败: {failed} 条")

    if successful > 0:
        avg_time = sum(r.get('processing_time', 0) for r in results) / len(results)
        print(f"⏱️  平均处理时间: {avg_time:.2f}秒/条")

    print("=" * 60)
    print("程序执行完毕！")