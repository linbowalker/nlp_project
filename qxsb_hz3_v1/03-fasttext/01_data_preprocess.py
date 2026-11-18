import jieba
from config import *


# 加载配置
conf = Config()


# 定义函数读取指定文件数据，并转为fasttext输入格式
def process_data(datapath, processed_datapath, is_char=True):
    # 读取原始文件
    with open(datapath, 'r', encoding='utf-8') as f:
        # 处理后数据写入新文件
        with open(processed_datapath, 'w', encoding='utf-8') as fw:
            for line in f.readlines():  # 此处.readlines()可以省略
                # 转换为fasttext格式:__label__字符串标签 分词后文本
                # 按行去除首尾多余字符
                line = line.strip()
                # 如果数据为空，则结束本轮循环,继续循环下一行
                if not line:
                    continue
                # 获取标签和文本
                text, label = line.split('\t')
                # 标签转换为整数索引
                label = int(label)
                # 获取标签字符串
                label_str = conf.id2class_dict[label]
                # 进行分词
                if is_char:
                    text_split = " ".join(list(text))
                else:
                    text_split = " ".join(jieba.lcut(text))
                # 打印测试结果
                # print(text_split)
                # print(label_str)
                # 构建fasttext格式
                ft_line = "__label__" + label_str + " " + text_split + "\n"
                # 写入文件
                fw.write(ft_line)


if __name__ == '__main__':
    # 字符级别处理
    process_data(conf.train_datapath, conf.process_train_datapath_char, is_char=True)
    process_data(conf.test_datapath, conf.process_test_datapath_char, is_char=True)
    process_data(conf.dev_datapath, conf.process_dev_datapath_char, is_char=True)

    # 分词级别处理
    process_data(conf.train_datapath, conf.process_train_datapath_word, is_char=False)
    process_data(conf.test_datapath, conf.process_test_datapath_word, is_char=False)
    process_data(conf.dev_datapath, conf.process_dev_datapath_word, is_char=False)
