import streamlit as st
import requests
import time
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="中文对话内容审核",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

CLASS_CATEGORIES = ["黑产广告", "欺诈", "博彩", "不违规", "谩骂引战", "低俗"]

CATEGORY_COLORS = {
    "黑产广告": "#dc3545",
    "欺诈": "#fd7e14",
    "博彩": "#6f42c1",
    "不违规": "#28a745",
    "谩骂引战": "#007bff",
    "低俗": "#e83e8c"
}

CATEGORY_DESCRIPTIONS = {
    "黑产广告": "非法推广、诈骗广告",
    "欺诈": "诈骗信息、虚假宣传",
    "博彩": "赌博信息、赌场宣传",
    "不违规": "正常对话、合规内容",
    "谩骂引战": "侮辱攻击、挑衅言论",
    "低俗": "不雅内容"
}

if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []
if 'classify_triggered' not in st.session_state:
    st.session_state.classify_triggered = False

# 注意：不再使用 input_text 状态管理输入，而是直接用 text_area 返回值
# 所以不需要初始化 input_text

st.markdown("""
<div style="text-align: center;">
    <h1>🛡️ 中文对话内容审核系统</h1>
    <p style="color: #666; margin-bottom: 1rem;">使用BERT模型自动识别文本中的违规内容</p>
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([3, 2], gap="medium")

with left_col:
    st.markdown("### 📝 输入待审核文本")

    # 关键：直接获取 text_area 的返回值，用于后续判断
    text = st.text_area(
        "输入需要审核的中文文本：",
        value="",  # 初始为空
        placeholder="在这里输入文本（可从右侧示例复制后粘贴）...",
        height=80,
        key="input_text_area",  # 使用明确 key
        label_visibility="collapsed"
    )

    # 操作按钮 —— 直接使用 `text` 变量判断是否禁用
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
                "🚀 开始审核",
                type="primary",
                width='stretch',
                disabled=not text.strip(),  # ✅ 直接使用 text
                key="classify_button"
        ):
            st.session_state.classify_triggered = True

    with col2:
        if st.button(
                "🔄 清空输入",
                width='stretch',
                key="clear_button"
        ):
            # Streamlit 无法直接清空 text_area，但可通过 rerun + 控制 value 实现
            # 但我们这里采用更简单方式：让用户手动删除，或复制新内容
            st.session_state.classify_triggered = False
            st.rerun()

    # 审核逻辑
    should_show_result = st.session_state.classify_triggered and text.strip()

    if should_show_result:
        st.session_state.classify_triggered = False

        st.divider()
        st.markdown("### 📊 审核结果")

        progress_placeholder = st.empty()
        status_placeholder = st.empty()

        with progress_placeholder.container():
            progress_bar = st.progress(0)
        status_placeholder.text("正在连接服务器...")

        start_time = time.time()

        try:
            progress_bar.progress(30)
            status_placeholder.text("正在分析文本内容...")

            response = requests.post(
                "http://127.0.0.1:8010/predict",
                json={'text': text},
                timeout=10
            )

            progress_bar.progress(80)

            if response.status_code == 200:
                try:
                    result = response.json()
                    pred_class = result.get("pred_class")
                    if pred_class not in CLASS_CATEGORIES:
                        raise ValueError("预测类别不在支持范围内")

                    progress_bar.progress(100)
                    time.sleep(0.1)
                    progress_placeholder.empty()
                    status_placeholder.empty()

                    color = CATEGORY_COLORS.get(pred_class, "gray")
                    is_safe = pred_class == "不违规"

                    col_result1, col_result2 = st.columns([3, 1])

                    with col_result1:
                        st.markdown(f"""
                        <div style='
                            padding: 16px;
                            border-radius: 8px;
                            background: {'#e8f5e9' if is_safe else '#fce8e6'};
                            border: 2px solid {color};
                            margin: 8px 0;
                        '>
                            <div style='font-size: 18px; font-weight: bold; margin-bottom: 8px;'>
                                <span style='color: {color}; font-size: 20px;'>
                                    {'✅' if is_safe else '🚫'} {pred_class}
                                </span>
                            </div>
                            <div style='color: #666;'>
                                {CATEGORY_DESCRIPTIONS.get(pred_class, '')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        if not is_safe:
                            st.warning("**处理建议**: 该内容涉嫌违规，建议进行处理")
                        else:
                            st.success("**处理建议**: 内容合规，无需处理")

                    with col_result2:
                        elapsed_time = (time.time() - start_time) * 1000
                        st.metric("处理耗时", f"{elapsed_time:.0f} ms")

                    history_entry = {
                        '时间': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        '文本': text[:50] + "..." if len(text) > 50 else text,
                        '分类结果': pred_class,
                        '耗时(ms)': f"{elapsed_time:.0f}"
                    }
                    st.session_state.predictions_history.append(history_entry)

                    if len(st.session_state.predictions_history) > 20:
                        st.session_state.predictions_history.pop(0)

                except (ValueError, KeyError, TypeError) as e:
                    progress_placeholder.empty()
                    status_placeholder.empty()
                    st.error(f"❌ 服务器返回数据格式错误: {str(e)}")
            else:
                progress_placeholder.empty()
                status_placeholder.empty()
                st.error(f"❌ 服务器错误: HTTP {response.status_code}")

        except requests.exceptions.ConnectionError:
            progress_placeholder.empty()
            status_placeholder.empty()
            st.error("❌ 无法连接到服务器，请检查服务是否启动")
        except Exception as e:
            progress_placeholder.empty()
            status_placeholder.empty()
            st.error(f"❌ 处理错误: {str(e)}")

    # 历史记录
    if st.session_state.predictions_history:
        st.divider()
        st.markdown("### 📈 审核历史记录")

        df_history = pd.DataFrame(st.session_state.predictions_history)
        st.dataframe(
            df_history,
            hide_index=True,
            column_config={
                "时间": st.column_config.TextColumn("时间", width="small"),
                "文本": st.column_config.TextColumn("文本内容", width="medium"),
                "分类结果": st.column_config.TextColumn("分类结果", width="small"),
                "耗时(ms)": st.column_config.TextColumn("耗时", width="small")
            }
        )

        if st.button("清空历史记录", type="secondary", width='stretch'):
            st.session_state.predictions_history = []
            st.rerun()

with right_col:
    st.markdown("### 📋 支持类别")
    for i in range(0, len(CLASS_CATEGORIES), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(CLASS_CATEGORIES):
                category = CLASS_CATEGORIES[i + j]
                color = CATEGORY_COLORS.get(category, "gray")
                with cols[j]:
                    st.markdown(f"""
                    <div style='
                        padding: 6px 8px;
                        margin: 3px 0;
                        border-radius: 5px;
                        background: {'#f8f9fa' if category != '不违规' else '#e8f5e9'};
                        border-left: 3px solid {color};
                        font-size: 12px;
                        line-height: 1.2;
                    '>
                        <strong style='color: {color}; font-size: 12px;'>{category}</strong><br>
                        <small style='color: #666; font-size: 10px;'>{CATEGORY_DESCRIPTIONS[category]}</small>
                    </div>
                    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🚨 快速示例")

    examples = [
        ("黑产广告", "微信刷单吗？"),
        ("欺诈", "靠谱项目，日入破千，想做的加"),
        ("博彩", "新用户注册送888彩金，稳赚不赔，日入过万"),
        ("谩骂引战", "你就是个废物垃圾，有种来单挑啊怂货"),
        # ("低俗", "想看更多刺激内容加V，深夜寂寞等你来聊"),
        ("不违规", "今天天气不错，适合出去散步锻炼")
    ]

    # ✅ 修复复制功能：使用更可靠的 navigator.clipboard（静默 + 无弹窗）
    for i, (category, example) in enumerate(examples):
        btn_id = f"copy_btn_{i}"
        # 转义特殊字符
        safe_example = example.replace('"', '\\"').replace("'", "\\'")

        st.markdown(f"""
        <button id="{btn_id}" style="
            width: 100%;
            padding: 0.25rem 0.5rem;
            font-size: 0.85rem;
            height: 32px;
            border: 1px solid #ced4da;
            border-radius: 0.25rem;
            background: white;
            cursor: pointer;
            text-align: left;
            margin: 0.05rem 0;
        ">{category}: {example[:60]}...</button>
        <script>
        document.getElementById("{btn_id}").onclick = async function() {{
            try {{
                await navigator.clipboard.writeText("{safe_example}");
                // 可选：显示成功提示（使用更友好的方式）
                const btn = document.getElementById("{btn_id}");
                const original = btn.innerHTML;
                btn.innerHTML = '✅ 已复制！';
                setTimeout(() => {{ btn.innerHTML = original; }}, 1000);
            }} catch (err) {{
                // 降级到 execCommand（旧浏览器）
                const textarea = document.createElement('textarea');
                textarea.value = "{safe_example}";
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                alert('已复制（旧方式）');
            }}
        }};
        </script>
        """, unsafe_allow_html=True)

# CSS 样式
st.markdown("""
<style>
    .main > div { padding-top: 0.2rem !important; padding-bottom: 0.2rem !important; }
    .stMarkdown h1 { margin: 0.2rem 0 !important; font-size: 1.6rem !important; }
    .stMarkdown h3 { margin: 0.8rem 0 0.4rem !important; font-size: 1.1rem !important; }
    .stTextArea textarea { height: 80px !important; min-height: 80px !important; max-height: 80px !important; font-size: 14px !important; }
    .stButton > button { margin: 0.05rem 0 !important; padding: 0.25rem 0.5rem !important; font-size: 0.85rem !important; height: 32px !important; }
    .dataframe { font-size: 12px !important; }
    [data-testid="column"] { padding: 0 0.3rem !important; }
    hr { margin: 0.6rem 0 !important; }
    .stAlert { padding: 0.4rem 0.6rem !important; margin: 0.4rem 0 !important; font-size: 0.85rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.1rem !important; }
    [data-testid="stMetricLabel"] { font-size: 0.8rem !important; }
    div[data-testid="stMarkdown"]:has(h1) { text-align: center !important; }
    .stButton button:disabled { opacity: 0.5 !important; cursor: not-allowed !important; }
</style>
""", unsafe_allow_html=True)

