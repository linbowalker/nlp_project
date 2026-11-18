import jieba
import pickle
from config import Config
import warnings
warnings.filterwarnings('ignore')

# 加载配置
conf = Config()
# 忽略警告信息

# 加载模型
with open(conf.rf_model_save_path, 'rb') as f:
    model = pickle.load(f)
# 加载向量化器
with open(conf.tfidf_model_save_path, 'rb') as f:
    tfidf = pickle.load(f)


def predict_fun(data):
    # jieba分词
    words = " ".join(jieba.lcut(data['text'])[:30])
    print("words-->", words)
    # 向量化
    features = tfidf.transform([words])
    print("features-->", features)
    # 预测
    # y_pred_id = model.predict(features)
    # print("y_pred_id-->", y_pred_id)
    y_pred_id = model.predict(features)[0]
    print("y_pred_id-->", y_pred_id)

    # 设置标签索引和名称对应关系
    id2class = {i: line.strip() for i, line in enumerate(open(conf.class_doc_path, encoding='utf-8'))}
    print("id2class-->", id2class)
    # 获取预测类别名称
    y_pred = id2class[y_pred_id]
    data["pred_class"] = y_pred
    return data


if __name__ == '__main__':
    data = {"text": "付出了才有回本，全网最低吃货上费在我这里 可以先来了解项目 在考虑做不做"}
    result = predict_fun(data)
    print(result)
