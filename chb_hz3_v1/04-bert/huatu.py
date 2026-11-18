import matplotlib.pyplot as plt

# 支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

# 数据
epochs = [1, 50, 100, 150]

# 1) 冻结 BERT 参数
val_f1_frozen = [25.40, 71.49, 74.27, 73.99]
test_f1_frozen = [29.22, 67.33, 69.82, 71.84]

# 2) 不冻结 BERT 参数
val_f1_unfrozen = [91.36, 94.26, 93.37, 92.50]
test_f1_unfrozen = [92.23, 92.28, 93.53, 94.41]

# 绘图
plt.figure(figsize=(10, 6))

# 冻结 BERT
plt.plot(epochs, val_f1_frozen, 'o--', label='冻结 BERT - 验证集 F1')
plt.plot(epochs, test_f1_frozen, 's--', label='冻结 BERT - 测试集 F1')

# 不冻结 BERT
plt.plot(epochs, val_f1_unfrozen, 'o-', label='微调 BERT - 验证集 F1')
plt.plot(epochs, test_f1_unfrozen, 's-', label='微调 BERT - 测试集 F1')

# 图表设置
plt.title('不同训练策略下 F1 分数随 epoch 的变化')
plt.xlabel('Epoch')
plt.ylabel('F1 分数 (%)')
plt.xticks(epochs)
plt.ylim(0, 100)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# 显示数值（可选）
for i, epoch in enumerate(epochs):
    plt.text(epoch, val_f1_frozen[i] + 1, f'{val_f1_frozen[i]:.2f}', ha='center', fontsize=8, color='blue')
    plt.text(epoch, test_f1_frozen[i] + 1, f'{test_f1_frozen[i]:.2f}', ha='center', fontsize=8, color='blue')
    plt.text(epoch, val_f1_unfrozen[i] + 1, f'{val_f1_unfrozen[i]:.2f}', ha='center', fontsize=8, color='red')
    plt.text(epoch, test_f1_unfrozen[i] + 1, f'{test_f1_unfrozen[i]:.2f}', ha='center', fontsize=8, color='red')

plt.tight_layout()
plt.show()