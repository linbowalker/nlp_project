import requests
# 定义接口地址
url = 'http://127.0.0.1:8008/predict'

try:
    # 测试调用api接口
    # 获取用户录入的新闻标题
    text = input("请输入新闻标题：")
    response = requests.post(url, json={'text': text})
    print("response1-->", response)
    # 从返回对象中获取json数据
    print('response2-->', response.json())

except Exception as e:
    print("Error occurred:", e)

