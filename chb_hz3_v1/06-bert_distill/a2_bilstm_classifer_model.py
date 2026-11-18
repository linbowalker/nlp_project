import torch
import torch.nn as nn
from config import Config
from transformers import BertTokenizer

conf = Config()


class BiLSTMModel(nn.Module):
    def __init__(self):
        # 调用父类初始化方法
        super().__init__()
        # 定义embedding
        self.embedding = nn.Embedding(conf.bert_config.vocab_size, conf.embed_size)
        # 定义lstm
        self.lstm = nn.LSTM(conf.embed_size, conf.hidden_size_lstm, conf.num_layers, bidirectional=True, batch_first=True)
        # 定义dropout
        self.dropout = nn.Dropout(conf.dropout)
        # 定义全连接层
        self.fc = nn.Linear(conf.hidden_size_lstm * 2, conf.num_classes)

    def forward(self, input_ids, attention_mask):
        """
        :param input_ids: 维度：[batch_size, seq_len]
        :param attention_mask: 维度：[batch_size, seq_len]
        :return:
        """
        # Embedding 层，获取ebedding词向量
        # [batch_size, seq_len, embed_size]
        embed = self.embedding(input_ids)
        # print("embed-->", embed, embed.shape)
        # 经过valid mask输出对应有效字符的embedding
        # 创建掩码，过滤 [CLS] (101) 和 [SEP] (102)
        cls_token_id = 101  # 动态获取 token ID
        sep_token_id = 102

        # print("input_ids-->", input_ids, input_ids.shape)
        # print("attention_mask-->", attention_mask, attention_mask.shape)
        # print("input_ids != cls_token_id-->", input_ids != cls_token_id)
        # print("input_ids != sep_token_id-->", input_ids != sep_token_id)
        # 把101和102都置为False: tensor([False,  True,  True... ,False])
        cls_sep_mask = (input_ids != cls_token_id) & (input_ids != sep_token_id)
        # print("cls_sep_mask-->", cls_sep_mask)
        # [batch_size, seq_len]
        valid_mask = attention_mask & cls_sep_mask
        # print("valid_mask-->", valid_mask, valid_mask.shape)
        # [batch_size, seq_len, 1]
        valid_mask_embed = valid_mask.unsqueeze(-1)
        # print("valid_mask_embed-->", valid_mask_embed)
        # 无效 token 的嵌入置为 0
        embed = embed * valid_mask_embed
        # print("embed-->", embed, embed.shape)

        # 经过BiLSTM 层 前向传播
        # [batch_size, seq_len, hidden_size*2]
        lstm_out, (hn, cn) = self.lstm(embed)
        # print("lstm_out-->", lstm_out, lstm_out.shape)
        # BERT的输出结果：pooler_output：当做一句话的整体token。除此之外，还有一个CLS（也可以当做这一句话的整体token）

        # 对整个句子有效字符（token数）进行平均。先求和，再除以token的数量
        valid_mask_out = valid_mask.unsqueeze(-1)
        # print("valid_mask_out-->", valid_mask_out)
        # [batch_size, seq_len, hidden_size*2]
        valid_lstm_out = lstm_out * valid_mask_out
        # print("valid_lstm_out-->", valid_lstm_out, valid_lstm_out.shape)
        # 求和
        # [batch_size, hidden_size*2]
        sum_hidden = valid_lstm_out.sum(dim=1)
        # print("sum_hidden-->", sum_hidden, sum_hidden.shape)
        # 有效 token 的数量，避免除以 0（加上一个极小值）
        # [batch_size, 1]
        valid_token_count = valid_mask_out.sum(dim=1) + 1e-8
        # print("valid_token_count-->", valid_token_count, valid_token_count.shape)
        # 平均池化
        # [batch_size, hidden_size*2]
        hidden = sum_hidden / valid_token_count
        # print("hidden-->", hidden, hidden.shape)

        # Dropout 和全连接层
        hidden = self.dropout(hidden)
        # [batch_size, num_classes]
        logits = self.fc(hidden)

        return logits


# 进行模型测试
def test_bilstm_model():
    # 编写测试数据
    model = BiLSTMModel()
    # 示例文本
    texts = ["我中意你", "你爱他"]

    tokenizer = BertTokenizer.from_pretrained(conf.bert_path)
    # 编码文本
    encoded_inputs = tokenizer(texts,
                               padding="max_length",
                               max_length=8,
                               return_tensors="pt")

    # 获取 input_ids 和 attention_mask
    input_ids = encoded_inputs["input_ids"]
    attention_mask = encoded_inputs["attention_mask"]

    # 预测
    logits = model(input_ids, attention_mask)
    print('logits-->', logits)  # 每一行对应一个样本，每个数字表示该样本属于某一类别的“得分”（logit），没有经过 softmax 归一化。

    # 获取预测概率
    probs = torch.softmax(logits, dim=-1)
    print('probs-->', probs)  # 归一化后该样本属于某类的概率（范围在 0~1 之间）,概率最高的就是预测结果

    # 获取最大元素对应的索引(类别)
    preds = torch.argmax(logits, dim=-1)
    print('preds-->', preds)  # 得到每个样本的预测类别。表示两个输入文本被模型预测为类别 6（从 0 开始计数）。


if __name__ == '__main__':
    test_bilstm_model()