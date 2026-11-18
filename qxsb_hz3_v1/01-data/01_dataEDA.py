from collections import Counter
import pandas as pd
from config import Config

# 创建配置对象，获取配置参数
conf = Config()

def data_eda(path):
    # 读取数据并查看基本信息
    # df_data = pd.read_csv(path, sep='\t', header=None, names=['text', 'label'])
    df_data = pd.read_csv(path, sep='\t', names=['text', 'label'])
    # 打印前10行
    print('df_data.head()-->', df_data.head(10))
    # 总数据量
    print('len(df_data)-->', len(df_data))
    # 查看类别数
    print('labels-->', df_data['label'].value_counts())

    # 统计标签分布
    counter = Counter(df_data['label'])
    print('counter-->', counter)
    # 打印
    for key, value in counter.items():
        print(key, value)

    # 计算标签比例
    all_count = len(df_data)  # 总次数
    for key, value in counter.items():  # key是标签  value是该标签出现的次数
        print(f"总量:{all_count}，标签{key}出现次数:{value}，标签{key}占比：{value / all_count:.2%}")

    # 第四步：分析文本长度
    # apply()依次对每个元素执行函数操作: 获取每行文本长度,作为一个新列拼接到原有数据中
    df_data['text_length'] = df_data['text'].apply(lambda x: len(x))
    print(df_data.head(10))
    # 查看新闻标题长度的分布情况
    print(df_data['text_length'].describe())
    print("\n文本长度统计：")
    print(f"平均长度：{df_data['text_length'].mean():.2f} 字符")  # 平均值
    print(f"长度标准差：{df_data['text_length'].std():.2f} 字符")  # 标准差
    print(f"最大长度：{df_data['text_length'].max()} 字符")  # 最大值
    print(f"最小长度：{df_data['text_length'].min()} 字符")  # 最小值

    # 统计最大，最小，平均的用处：可以指导模型输入。
    # 因为这里长度最大是38，最小是8，平均值是19.21，所以，可以选择20左右甚至往上。



if __name__ == '__main__':
    # 获取训练集路径
    data_eda(conf.train_path)
    # data_eda(conf.dev_path)
    # data_eda(conf.test_path)
