class Config:
    def __init__(self):
        self.root_path = r'F:\workspace\chb_hz3/'
        # 原始数据路径
        self.train_datapath = self.root_path + '01-data/train.txt'
        self.test_datapath = self.root_path + '01-data/test.txt'
        self.dev_datapath = self.root_path + '01-data/dev.txt'
        # 类别文档
        self.class_doc_path = self.root_path + "01-data/class.txt"

        # 数据处理保存路径
        # 字符级别fasttext
        self.process_train_datapath_char = self.root_path + "03-fasttext/final_data/train_process_char.txt"
        self.process_test_datapath_char = self.root_path + "03-fasttext/final_data/test_process_char.txt"
        self.process_dev_datapath_char = self.root_path + "03-fasttext/final_data/dev_process_char.txt"

        # 词级别fasttext
        self.process_train_datapath_word = self.root_path + "03-fasttext/final_data/train_process_word.txt"
        self.process_test_datapath_word = self.root_path + "03-fasttext/final_data/test_process_word.txt"
        self.process_dev_datapath_word = self.root_path + "03-fasttext/final_data/dev_process_word.txt"

        # 处理完的数据（用于训练）
        self.final_data = self.root_path + '03-fasttext/final_data'

        # 模型路径
        self.ft_model_save_path = self.root_path + '03-fasttext/save_models'

        # 类别字典 {标签索引:标签名称}
        self.id2class_dict = {i: line.strip() for i, line in enumerate(open(self.class_doc_path, encoding='utf-8'))}


if __name__ == '__main__':
    conf = Config()
    print('conf.train_datapath-->', conf.train_datapath)
    print('conf.test_datapath-->', conf.test_datapath)
    print('conf.dev_datapath-->', conf.dev_datapath)
    print('conf.id2class_dict-->', conf.id2class_dict)
