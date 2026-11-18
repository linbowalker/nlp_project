# 导入工具包
import fasttext
from config import Config


# 获取时间
conf = Config()

# 1、模型训练
model = fasttext.train_supervised(input=conf.process_train_datapath_word, seed=42)

# 2、模型保存
model_path = conf.ft_model_save_path + "/model_word_1_default1.bin"
model.save_model(model_path)

# 3、模型预测
print(model.predict("日本 地震 ： 金吉列 关注 在 日 学子 系列报道"))

# 4、模型词表的查看
print(model.words[:10])

# 5、模型子词查看
print(model.get_subwords("日本"))
# 输出模型维度
print(model.get_dimension())

# 6、模型评估
print(model.test(conf.process_test_datapath_word))
