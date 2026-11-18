import jieba
import pandas as pd
from config import Config

# 加载配置类对象
conf = Config()


def process_data(datapath, processed_datapath):
    # 读取数据,指定列名为text和label
    df_data = pd.read_csv(datapath, sep='\t', header=None, names=['text', 'label'])
    print('df_data-->', df_data.head())

    # 进行分词预处理
    # 把结巴分词拼接后结果作为新列拼接原数据集,最后保存
    # 其中apply功能是: 对输入文本进行结巴分词，获取前30个词并用空格连接
    df_data['words'] = df_data['text'].apply(lambda x: " ".join(jieba.lcut(x)[:30]))
    print(df_data.head())

    # 保存数据
    df_data.to_csv(processed_datapath, sep='\t', index=False, header=True)


if __name__ == '__main__':
    # 保存处理后训练数据
    process_data(conf.train_datapath, conf.process_train_datapath)
    # 保存处理后测试数据
    process_data(conf.test_datapath, conf.process_test_datapath)
    # 保存处理后验证数据
    process_data(conf.dev_datapath, conf.process_dev_datapath)
