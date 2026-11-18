input_json = './Simplified_Chinese_Multi-Emotion_Dialogue_Dataset/Simplified_Chinese_Multi-Emotion_Dialogue_Dataset.csv'
output_txt = 'output.txt'
class_txt = 'class.txt'

label_to_id = {}
labels_order = []

# 第一步：收集所有有效 label（跳过 header 行）
with open(input_json, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.rsplit(',', 1)
        if len(parts) != 2:
            continue
        text, label = parts[0], parts[1]

        # 跳过 header 行（例如 "text,label"）
        if text == "text" and label == "label":
            continue

        if label not in label_to_id:
            label_to_id[label] = len(labels_order)
            labels_order.append(label)

# 第二步：写入 class.txt（纯类别名，每行一个）
with open(class_txt, 'w', encoding='utf-8') as f:
    for label in labels_order:
        f.write(label + '\n')

# 第三步：转换数据（跳过 header，只写纯样本）
with open(input_json, 'r', encoding='utf-8') as fin, \
     open(output_txt, 'w', encoding='utf-8') as fout:

    for line in fin:
        line = line.strip()
        if not line:
            continue
        parts = line.rsplit(',', 1)
        if len(parts) != 2:
            continue
        text, label = parts[0], parts[1]

        # 跳过 header
        if text == "text" and label == "label":
            continue

        # 如果之前已构建映射（应该都在）
        if label in label_to_id:
            label_id = label_to_id[label]
            fout.write(f"{text}\t{label_id}\n")

print("✅ 转换完成！")
print(f"   - 数据已保存至: {output_txt}（无 header，直接从样本开始）")
print(f"   - 类别文件: {class_txt}")
print(f"   - 共 {len(labels_order)} 个类别，{sum(1 for _ in open(output_txt, 'r', encoding='utf-8'))} 条样本。")