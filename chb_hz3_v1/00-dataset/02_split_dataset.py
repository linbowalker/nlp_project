import random
import os
from tqdm import tqdm

def main():
    input_file = 'output.txt'
    train_file = 'train.txt'
    dev_file = 'dev.txt'
    test_file = 'test.txt'

    # 可选：设置随机种子以保证可复现
    random.seed(42)

    # 读取所有行
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 随机打乱
    random.shuffle(lines)

    total = len(lines)
    train_end = int(0.9 * total)      # 18/20 = 90%
    dev_end = train_end + int(0.05 * total)  # +5% → 95%

    train_lines = lines[:train_end]
    dev_lines = lines[train_end:dev_end]
    test_lines = lines[dev_end:]

    # 写入函数（带进度条）
    def write_lines(filename, lines_list):
        with open(filename, 'w', encoding='utf-8') as f:
            for line in tqdm(lines_list, desc=f"Writing {filename}", leave=False):
                f.write(line)

    # 写入三个文件（保留原始格式：文本\t标签）
    write_lines(train_file, train_lines)
    write_lines(dev_file, dev_lines)
    write_lines(test_file, test_lines)

    print(f"\n✅ 划分完成！")
    print(f"  - 训练集 (90%): {len(train_lines)} 行 → {train_file}")
    print(f"  - 验证集 (5%): {len(dev_lines)} 行 → {dev_file}")
    print(f"  - 测试集 (5%): {len(test_lines)} 行 → {test_file}")

if __name__ == '__main__':
    main()