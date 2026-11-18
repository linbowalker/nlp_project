class Config:
    def __init__(self):
        self.root_path = r'F:\workspace\qxsb_hz3'
        self.train_path = self.root_path + '/01-data/train.txt'
        self.dev_path = self.root_path + '/01-data/dev.txt'
        self.test_path = self.root_path + '/01-data/test.txt'


if __name__ == '__main__':
    # 测试配置文件
    conf = Config()
    # 打印参数路径
    print(conf.train_path)
    print(conf.dev_path)
    print(conf.test_path)
