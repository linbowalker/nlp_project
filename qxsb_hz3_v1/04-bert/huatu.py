import matplotlib.pyplot as plt

# 支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

# 数据（qxsb 数据集）
epochs = [1, 10, 20, 25, 50]

# 冻结 BERT（仅训练分类头）
frozen_val_f1 = [0.1859, 0.5539, 0.6285, 0.6271, 0.7392]
frozen_test_f1 = [0.1116, 0.5748, 0.5697, 0.6350, 0.6689]

# 微调 BERT（打开参数更新）
unfrozen_val_f1 = [0.8220, 0.8476, 0.8245, 0.8534, 0.8317]
unfrozen_test_f1 = [0.8477, 0.8579, 0.8713, 0.8316, 0.8318]

# 转换为百分比（可选，便于阅读）
frozen_val_f1 = [x * 100 for x in frozen_val_f1]
frozen_test_f1 = [x * 100 for x in frozen_test_f1]
unfrozen_val_f1 = [x * 100 for x in unfrozen_val_f1]
unfrozen_test_f1 = [x * 100 for x in unfrozen_test_f1]

# 绘图
plt.figure(figsize=(10, 6))

# 冻结 BERT
plt.plot(epochs, frozen_val_f1, 'o--', label='冻结 BERT - 验证集 F1', color='tab:blue')
plt.plot(epochs, frozen_test_f1, 's--', label='冻结 BERT - 测试集 F1', color='tab:cyan')

# 微调 BERT
plt.plot(epochs, unfrozen_val_f1, 'o-', label='微调 BERT - 验证集 F1', color='tab:red')
plt.plot(epochs, unfrozen_test_f1, 's-', label='微调 BERT - 测试集 F1', color='tab:orange')

# 图表设置
plt.title('qxsb 数据集：冻结 vs 微调 BERT 的 F1 分数对比')
plt.xlabel('Epoch')
plt.ylabel('F1 分数 (%)')
plt.xticks(epochs)
plt.ylim(0, 100)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# 可选：在点上标注数值（保留一位小数）
for i, epoch in enumerate(epochs):
    plt.text(epoch, frozen_val_f1[i] + 1.2, f'{frozen_val_f1[i]:.1f}', ha='center', fontsize=8, color='blue')
    plt.text(epoch, frozen_test_f1[i] + 1.2, f'{frozen_test_f1[i]:.1f}', ha='center', fontsize=8, color='cyan')
    plt.text(epoch, unfrozen_val_f1[i] + 1.2, f'{unfrozen_val_f1[i]:.1f}', ha='center', fontsize=8, color='red')
    plt.text(epoch, unfrozen_test_f1[i] + 1.2, f'{unfrozen_test_f1[i]:.1f}', ha='center', fontsize=8, color='orange')

plt.tight_layout()
plt.show()