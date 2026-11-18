class Config:
    def __init__(self):
        self.root_path = r'F:\workspace\chb_hz3/'
        # 原始数据路径
        self.train_datapath = self.root_path + '01-data/train.txt'
        self.test_datapath = self.root_path + '01-data/test.txt'
        self.dev_datapath = self.root_path + '01-data/dev.txt'
        # 类别文档
        self.class_doc_path = self.root_path + "01-data/class.txt"
        # 停用词路径
        self.stop_words_path = self.root_path + "01-data/stopwords.txt"

        # 处理后的数据路径
        self.process_train_datapath = self.root_path + "02-rf/final_data/train_process.txt"
        self.process_test_datapath = self.root_path + "02-rf/final_data/test_process.txt"
        self.process_dev_datapath = self.root_path + "02-rf/final_data/dev_process.txt"


        # 保存模型路径
        self.rf_model_save_path = self.root_path + r"02-rf/save_model/rf_model1.pkl"
        self.tfidf_model_save_path = self.root_path + r"02-rf/save_model/tfidf_model1.pkl"
        # 模型预测结果
        self.model_predict_result = self.root_path + r"02-rf/result/predict_result.txt"


if __name__ == '__main__':
    conf = Config()
    print('conf-->', conf.train_datapath)