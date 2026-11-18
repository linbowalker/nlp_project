import streamlit as st
import requests
import time

st.title("中文有害内容检测")

text = st.text_input("请输入要查询分类的文本:")

# 初始化 session_state
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_time" not in st.session_state:
    st.session_state.last_time = None

if st.button("基于随机森林模型获取分类！"):
    if not text.strip():
        st.warning("请输入文本！")
    else:
        try:
            start_time = time.time()
            response = requests.post('http://192.168.39.156:8008/predict', json={'text': text})
            elapsed_ms = (time.time() - start_time) * 1000

            # ✅ 关键：把结果存入 session_state
            st.session_state.last_result = response.json()["pred_class"]
            st.session_state.last_time = elapsed_ms

        except Exception as e:
            st.session_state.last_result = f"错误: {str(e)}"
            st.session_state.last_time = None

# ✅ 在按钮外部显示结果（但数据来自 session_state，可持久更新）
if st.session_state.last_result is not None:
    st.write("⏱️ 耗时：", st.session_state.last_time, "ms")
    st.write("🔍 预测结果：", st.session_state.last_result)