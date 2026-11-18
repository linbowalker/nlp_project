import json
import re
from tqdm import tqdm
from collections import Counter

def clean_text(text):
    """清洗文本，仅保留汉字、字母、数字、常见标点和空格"""
    if not isinstance(text, str):
        text = str(text)

    allowed = (
        r'\u4e00-\u9fff'      # 汉字
        r'a-zA-Z'             # 英文字母
        r'0-9'                # 数字
        r'，。！？；：""''（）【】《》〈〉·'  # 中文标点
        r'.!?;:\'"(),\-–—\[\]{}\/\\%&=+*'  # 英文标点及常用符号
        r' '                  # 普通空格
    )
    pattern = re.compile(f'[{allowed}]+', re.UNICODE)
    matches = pattern.findall(text)
    cleaned = ''.join(matches)
    cleaned = re.sub(r' +', ' ', cleaned).strip()
    return cleaned if cleaned else "[EMPTY]"

def main():
    input_json = './ChineseHarm-bench/bench.json'
    output_txt = 'output.txt'
    class_txt = 'class.txt'

    # 1. 读取数据
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print("❌ 输入文件为空！")
        return

    # 2. 收集所有标签（保留原始顺序），并动态统计真实数量
    label_counter = Counter()  # 动态统计
    unique_labels = []
    label2id = {}

    # 第一遍：确定唯一标签顺序
    for item in data:
        if '标签' in item:
            label = item['标签']
            if label not in label2id:
                label2id[label] = len(unique_labels)
                unique_labels.append(label)
            label_counter[label] += 1  # 累加真实数量

    # 3. 写入 class.txt
    with open(class_txt, 'w', encoding='utf-8') as f:
        for label in unique_labels:
            f.write(f"{label}\n")

    # 4. 写入 output.txt（保留所有样本）
    with open(output_txt, 'w', encoding='utf-8') as f:
        for item in tqdm(data, desc="Converting", unit="item"):
            raw_text = item.get('文本', '')
            label = item.get('标签', '[NO_LABEL]')
            cleaned_text = clean_text(raw_text)
            label_id = label2id.get(label, -1)  # 若标签不在 mapping 中，用 -1
            f.write(f"{cleaned_text}\t{label_id}\n")

    # 5. 在终端打印标签分布统计（像你截图那样）
    total = sum(label_counter.values())
    print("\n📊 标签分布统计（真实数量）：")
    for label in unique_labels:
        count = label_counter[label]
        pct = count / total * 100
        print(f"  {label}: {count} ({pct:.2f}%)")

    print(f"\n✅ 转换完成！")
    print(f"  - 输出文件: {output_txt}")
    print(f"  - 标签列表: {class_txt}")
    print(f"  - 总样本数: {total}")

if __name__ == '__main__':
    main()