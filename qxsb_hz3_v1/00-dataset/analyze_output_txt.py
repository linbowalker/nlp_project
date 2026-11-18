# -*- coding: utf-8 -*-
"""
情绪分类数据集分析脚本（终极无乱码 + 无错误版）
- 修复 plt.cos 错误
- 彻底解决中文显示为方框问题
- 生成高清 PNG + PDF 图表
"""

import os
import warnings

warnings.filterwarnings("ignore", message="Glyph.*missing from font.*Arial")
warnings.filterwarnings("ignore", message=".*Passing `palette` without assigning `hue`.*")

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import numpy as np  # 确保在使用前导入

# ===== 加载 SimHei 字体 =====
simhei_path = "C:/Windows/Fonts/simhei.ttf"
if os.path.exists(simhei_path):
    font_prop = fm.FontProperties(fname=simhei_path)
else:
    font_prop = fm.FontProperties(family='SimHei')
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']

plt.rcParams['axes.unicode_minus'] = False

# ===== 类别映射 =====
label_id_to_name = {
    0: "平静",
    1: "开心",
    2: "伤心",
    3: "生气",
    4: "惊讶",
    5: "厌恶",
    6: "疑问",
    7: "关心"
}
all_classes = list(label_id_to_name.values())


# ===== 数据加载 =====
def load_dataset_from_txt(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ 文件未找到: {os.path.abspath(file_path)}")

    texts, labels = [], []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.rsplit('\t', 1)
            if len(parts) != 2:
                continue
            text, label_str = parts
            try:
                label_id = int(label_str)
                texts.append(text)
                labels.append(label_id)
            except ValueError:
                continue
    return texts, labels


# ===== 主分析函数 =====
def analyze_and_plot(file_path="output.txt", save_dir="plots"):
    os.makedirs(save_dir, exist_ok=True)
    print(f"📥 正在读取数据: {os.path.abspath(file_path)}")

    texts, label_ids = load_dataset_from_txt(file_path)
    if not texts:
        print("❌ 未读取到有效样本！")
        return

    label_names = [label_id_to_name.get(lid, f"未知({lid})") for lid in label_ids]
    df = pd.DataFrame({'text': texts, 'label_id': label_ids, 'label_name': label_names})
    class_counts = df['label_name'].value_counts().reindex(all_classes, fill_value=0)
    total = len(df)

    print(f"\n📊 总样本数: {total}")
    print("-" * 30)
    for label in all_classes:
        count = class_counts[label]
        ratio = count / total * 100 if total > 0 else 0
        print(f"{label:>6}: {count:>6} ({ratio:>5.1f}%)")

    sns.set(style="whitegrid")
    colors = sns.color_palette("colorblind", len(all_classes))

    # ========== 柱状图 ==========
    plt.figure(figsize=(11, 6.5))
    bars = plt.bar(range(len(class_counts)), class_counts.values, color=colors)

    plt.title("情绪类别样本分布", fontproperties=font_prop, fontsize=20, weight='bold', pad=20)
    plt.xlabel("情绪类别", fontproperties=font_prop, fontsize=15)
    plt.ylabel("样本数量", fontproperties=font_prop, fontsize=15)
    plt.xticks(range(len(class_counts)), class_counts.index,
               rotation=30, ha='right', fontsize=13, fontproperties=font_prop)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    for i, (bar, count) in enumerate(zip(bars, class_counts.values)):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(class_counts.values) * 0.01,
            str(count),
            ha='center', va='bottom',
            fontsize=13, weight='bold',
            fontproperties=font_prop
        )

    plt.tight_layout()
    bar_png = os.path.join(save_dir, "class_distribution_bar.png")
    bar_pdf = os.path.join(save_dir, "class_distribution_bar.pdf")
    plt.savefig(bar_png, dpi=300, bbox_inches='tight')
    plt.savefig(bar_pdf, bbox_inches='tight')
    plt.close()

    # ========== 饼图 ==========（关键：使用 np.cos / np.sin）
    plt.figure(figsize=(9, 9))

    # 生成饼图扇区
    wedges, _ = plt.pie(
        class_counts.values,
        startangle=140,
        colors=colors,
        textprops={'fontsize': 13}
    )

    # 手动添加标签和百分比（确保字体正确）
    for i, (wedge, label) in enumerate(zip(wedges, class_counts.index)):
        pct = class_counts.values[i] / total * 100
        angle = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1

        # 百分比位置（在扇区内）
        x = 0.75 * np.cos(np.deg2rad(angle))
        y = 0.75 * np.sin(np.deg2rad(angle))
        plt.text(x, y, f'{pct:.1f}%',
                 ha='center', va='center',
                 fontsize=12, weight='bold', color='white',
                 fontproperties=font_prop)

        # 类别标签位置（在扇区外）
        label_angle = angle
        if label_angle > 90 or label_angle < -90:
            label_angle += 180
        lx = 1.2 * np.cos(np.deg2rad(label_angle))
        ly = 1.2 * np.sin(np.deg2rad(label_angle))
        plt.text(lx, ly, label,
                 ha='center', va='center',
                 fontsize=12, color='black',
                 fontproperties=font_prop)

    plt.title("情绪类别样本占比", fontproperties=font_prop, fontsize=20, weight='bold', pad=20)
    plt.tight_layout()
    pie_png = os.path.join(save_dir, "class_distribution_pie.png")
    pie_pdf = os.path.join(save_dir, "class_distribution_pie.pdf")
    plt.savefig(pie_png, dpi=300, bbox_inches='tight')
    plt.savefig(pie_pdf, bbox_inches='tight')
    plt.close()

    # ========== 均衡性分析 ==========
    min_count = class_counts.min()
    max_count = class_counts.max()
    print(f"\n⚖️  均衡性分析：")
    print(f"  最多样本: {class_counts.idxmax()} ({max_count})")
    print(f"  最少样本: {class_counts.idxmin()} ({min_count})")

    if total > 0 and min_count > 0:
        ratio = max_count / min_count
        if ratio > 5:
            print("  ⚠️  严重不均衡（建议加权/采样）")
        elif ratio > 2:
            print("  ⚠️  中度不均衡（建议训练加权）")
        else:
            print("  ✅ 数据分布较均衡")


# ===== 主程序 =====
if __name__ == "__main__":
    analyze_and_plot(file_path="output.txt")