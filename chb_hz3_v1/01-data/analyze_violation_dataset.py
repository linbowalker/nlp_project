# -*- coding: utf-8 -*-
"""
违规内容分类数据集分析脚本（6类别）
- 类别：黑产广告、欺诈、博彩、不违规、谩骂引战、低俗
- 自动分析样本分布，生成高清图表（PNG + PDF）
- 中文显示完美，无乱码，无警告
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
import numpy as np

# ===== 加载 SimHei 字体（Windows）=====
simhei_path = "C:/Windows/Fonts/simhei.ttf"
if os.path.exists(simhei_path):
    font_prop = fm.FontProperties(fname=simhei_path)
else:
    font_prop = fm.FontProperties(family='SimHei')
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ===== 6 类别映射（请根据你的实际标签顺序调整！）=====
label_id_to_name = {
    0: "黑产广告",
    1: "欺诈",
    2: "博彩",
    3: "不违规",
    4: "谩骂引战",
    5: "低俗"
}
all_classes = list(label_id_to_name.values())


# ===== 数据加载 =====
def load_dataset_from_txt(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ 文件未找到: {os.path.abspath(file_path)}")

    texts, labels = [], []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
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
def analyze_and_plot(file_path="output.txt", save_dir="plots_violation"):
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
        print(f"{label:>8}: {count:>6} ({ratio:>5.1f}%)")

    # 绘图设置
    sns.set(style="whitegrid")
    colors = sns.color_palette("colorblind", len(all_classes))

    # ========== 柱状图 ==========
    plt.figure(figsize=(10, 6))
    bars = plt.bar(range(len(class_counts)), class_counts.values, color=colors)

    plt.title("违规内容类别样本分布", fontproperties=font_prop, fontsize=18, weight='bold', pad=15)
    plt.xlabel("违规类别", fontproperties=font_prop, fontsize=14)
    plt.ylabel("样本数量", fontproperties=font_prop, fontsize=14)
    plt.xticks(range(len(class_counts)), class_counts.index,
               rotation=30, ha='right', fontsize=12, fontproperties=font_prop)
    plt.yticks(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)

    for bar, count in zip(bars, class_counts.values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(class_counts.values) * 0.01,
            str(count),
            ha='center', va='bottom',
            fontsize=12, weight='bold',
            fontproperties=font_prop
        )

    plt.tight_layout()
    bar_png = os.path.join(save_dir, "violation_distribution_bar.png")
    bar_pdf = os.path.join(save_dir, "violation_distribution_bar.pdf")
    plt.savefig(bar_png, dpi=300, bbox_inches='tight')
    plt.savefig(bar_pdf, bbox_inches='tight')
    plt.close()

    # ========== 饼图 ==========
    plt.figure(figsize=(8, 8))
    wedges, _ = plt.pie(
        class_counts.values,
        startangle=140,
        colors=colors
    )

    for i, (wedge, label) in enumerate(zip(wedges, class_counts.index)):
        pct = class_counts.values[i] / total * 100
        angle = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1

        # 百分比（扇区内）
        x = 0.7 * np.cos(np.deg2rad(angle))
        y = 0.7 * np.sin(np.deg2rad(angle))
        plt.text(x, y, f'{pct:.1f}%',
                 ha='center', va='center',
                 fontsize=11, weight='bold', color='white',
                 fontproperties=font_prop)

        # 类别标签（扇区外）
        label_angle = angle
        if label_angle > 90 or label_angle < -90:
            label_angle += 180
        lx = 1.15 * np.cos(np.deg2rad(label_angle))
        ly = 1.15 * np.sin(np.deg2rad(label_angle))
        plt.text(lx, ly, label,
                 ha='center', va='center',
                 fontsize=11, color='black',
                 fontproperties=font_prop)

    plt.title("违规内容类别样本占比", fontproperties=font_prop, fontsize=18, weight='bold', pad=15)
    plt.tight_layout()
    pie_png = os.path.join(save_dir, "violation_distribution_pie.png")
    pie_pdf = os.path.join(save_dir, "violation_distribution_pie.pdf")
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