import streamlit as st
import requests
import time
import pandas as pd
from datetime import datetime

# ===== 页面配置 =====
st.set_page_config(
    page_title="中文文本情绪识别",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== 情绪类别与配置 =====
CLASS_CATEGORIES = ["平静", "开心", "伤心", "生气", "惊讶", "厌恶", "疑问", "关心"]

CATEGORY_COLORS = {
    "平静": "#28a745",
    "开心": "#ffc107",
    "伤心": "#6c757d",
    "生气": "#dc3545",
    "惊讶": "#007bff",
    "厌恶": "#6f42c1",
    "疑问": "#20c997",
    "关心": "#f84d8a",
}

CATEGORY_DESCRIPTIONS = {
    "平静": "语气平和，无明显情绪波动",
    "开心": "表达喜悦、满足或积极情绪",
    "伤心": "流露悲伤、失落或沮丧",
    "生气": "带有愤怒、不满或指责",
    "惊讶": "表现出意外、震惊或难以置信",
    "厌恶": "表达反感、鄙夷或排斥",
    "疑问": "提出问题或表示疑惑",
    "关心": "体现关切、体贴或担忧"
}

EMOJI_MAP = {
    "平静": "😌",
    "开心": "😄",
    "伤心": "😢",
    "生气": "😠",
    "惊讶": "😮",
    "厌恶": "😖",
    "疑问": "🤔",
    "关心": "🥺"
}

# ===== 初始化会话状态 =====
if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []
if 'classify_triggered' not in st.session_state:
    st.session_state.classify_triggered = False
if 'input_text' not in st.session_state:          # ✅ 新增：管理输入框内容
    st.session_state.input_text = ""

# ===== 页面标题 =====
st.markdown("""
<div style="text-align: center;">
    <h1>🎭 中文文本情绪识别系统</h1>
    <p style="color: #666; margin-bottom: 1rem;">使用深度学习模型自动识别文本中蕴含的情绪</p>
</div>
""", unsafe_allow_html=True)

# ===== 主体布局 =====
left_col, right_col = st.columns([3, 2], gap="medium")

with left_col:
    st.markdown("### 📝 输入待分析文本")

    # ✅ 关键：value 绑定到 session_state
    text = st.text_area(
        "输入需要分析情绪的中文文本：",
        value=st.session_state.input_text,
        placeholder="在这里输入文本（可从右侧示例复制后粘贴）...",
        height=80,
        key="input_text_area",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "🧠 识别情绪",
            type="primary",
            width='stretch',
            disabled=not text.strip(),
            key="classify_button"
        ):
            st.session_state.classify_triggered = True
            # 可选：同步输入状态（非必须，因 value 已绑定）
            st.session_state.input_text = text

    with col2:
        if st.button(
            "🔄 清空输入",
            width='stretch',
            key="clear_button"
        ):
            st.session_state.input_text = ""        # ✅ 清空状态
            st.session_state.classify_triggered = False
            st.rerun()  # 强制刷新，使 text_area 重置

    # 情绪识别逻辑
    should_show_result = st.session_state.classify_triggered and text.strip()

    if should_show_result:
        st.session_state.classify_triggered = False

        st.divider()
        st.markdown("### 📊 情绪分析结果")

        progress_placeholder = st.empty()
        status_placeholder = st.empty()

        with progress_placeholder.container():
            progress_bar = st.progress(0)
        status_placeholder.text("正在连接服务器...")

        start_time = time.time()

        try:
            progress_bar.progress(30)
            status_placeholder.text("正在分析文本情绪...")

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
                        raise ValueError("预测情绪不在支持范围内")

                    progress_bar.progress(100)
                    time.sleep(0.1)
                    progress_placeholder.empty()
                    status_placeholder.empty()

                    color = CATEGORY_COLORS.get(pred_class, "gray")
                    is_neutral = pred_class == "平静"
                    emoji = EMOJI_MAP.get(pred_class, "😶")

                    col_result1, col_result2 = st.columns([3, 1])

                    with col_result1:
                        st.markdown(f"""
                        <div style='
                            padding: 16px;
                            border-radius: 8px;
                            background: {'#e8f5e9' if is_neutral else '#f8f9fa'};
                            border: 2px solid {color};
                            margin: 8px 0;
                        '>
                            <div style='font-size: 18px; font-weight: bold; margin-bottom: 8px;'>
                                <span style='color: {color}; font-size: 22px;'>{emoji}</span> {pred_class}
                            </div>
                            <div style='color: #666;'>
                                {CATEGORY_DESCRIPTIONS.get(pred_class, '')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        if pred_class in ["伤心", "生气", "厌恶"]:
                            st.warning("**情绪提示**: 该文本带有负面情绪，建议关注沟通方式")
                        elif pred_class in ["开心", "关心"]:
                            st.success("**情绪提示**: 文本情绪积极，适合继续互动")
                        else:
                            st.info("**情绪提示**: 文本情绪中性或复杂，可结合上下文判断")

                    with col_result2:
                        elapsed_time = (time.time() - start_time) * 1000
                        st.metric("处理耗时", f"{elapsed_time:.0f} ms")

                    # 保存历史（含 emoji）
                    history_entry = {
                        '时间': datetime.now().strftime("%H:%M:%S"),
                        '文本': text[:50] + "..." if len(text) > 50 else text,
                        '情绪': f"{EMOJI_MAP.get(pred_class, '')} {pred_class}",
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
        st.markdown("### 📈 分析历史记录")

        df_history = pd.DataFrame(st.session_state.predictions_history)
        st.dataframe(
            df_history,
            hide_index=True,
            column_config={
                "时间": st.column_config.TextColumn("时间", width="small"),
                "文本": st.column_config.TextColumn("文本内容", width="medium"),
                "情绪": st.column_config.TextColumn("识别情绪", width="small"),
                "耗时(ms)": st.column_config.TextColumn("耗时", width="small")
            }
        )

        if st.button("清空历史记录", type="secondary", width='stretch'):
            st.session_state.predictions_history = []
            st.rerun()

# ===== 右侧栏 =====
with right_col:
    st.markdown("### 🎭 支持的情绪类别")
    for i in range(0, len(CLASS_CATEGORIES), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(CLASS_CATEGORIES):
                category = CLASS_CATEGORIES[i + j]
                color = CATEGORY_COLORS.get(category, "gray")
                emoji = EMOJI_MAP.get(category, "❓")
                if category == "平静":
                    bg = "#e8f5e9"
                elif category in ["开心", "关心"]:
                    bg = "#fff8e1"
                elif category in ["伤心", "生气", "厌恶"]:
                    bg = "#fce8e6"
                else:
                    bg = "#f8f9fa"

                with cols[j]:
                    st.markdown(f"""
                    <div style='
                        padding: 6px 8px;
                        margin: 3px 0;
                        border-radius: 5px;
                        background: {bg};
                        border-left: 3px solid {color};
                        font-size: 12px;
                        line-height: 1.2;
                    '>
                        <strong style='color: {color}; font-size: 12px;'>{emoji} {category}</strong><br>
                        <small style='color: #666; font-size: 10px;'>{CATEGORY_DESCRIPTIONS[category]}</small>
                    </div>
                    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 💬 快速示例")

    examples = [
        ("平静", "今天按照计划完成了所有任务。"),
        ("开心", "太棒了！终于通过了面试！"),
        ("伤心", "他已经不是我曾经认为的那个人，而我也不再是我自己。"),
        ("生气", "说了多少次都记不住，真是气死我了！"),
        ("惊讶", "什么？你居然中了五百万？！"),
        ("厌恶", "这种自私自利的人真是让人作呕。"),
        ("疑问", "我这样做真的对吗？"),
        ("关心", "你最近是不是太累了？要注意休息啊。")
    ]

    for i, (category, example) in enumerate(examples):
        btn_id = f"copy_btn_{i}"
        safe_example = example.replace('"', '\\"').replace("'", "\\'")
        display_text = example[:30] + "..." if len(example) > 30 else example
        emoji = EMOJI_MAP.get(category, "")

        st.markdown(f"""
        <button id="{btn_id}" style="
            width: 100%;
            padding: 0.25rem 0.5rem;
            font-size: 0.85rem;
            height: auto;
            min-height: 32px;
            border: 1px solid #ced4da;
            border-radius: 0.25rem;
            background: white;
            cursor: pointer;
            text-align: left;
            margin: 0.05rem 0;
            white-space: normal;
            line-height: 1.3;
        ">{emoji} {category}: {display_text}</button>
        <script>
        document.getElementById("{btn_id}").onclick = async function() {{
            try {{
                await navigator.clipboard.writeText("{safe_example}");
                const btn = document.getElementById("{btn_id}");
                const original = btn.innerHTML;
                btn.innerHTML = '✅ 已复制！';
                setTimeout(() => {{ btn.innerHTML = original; }}, 1000);
            }} catch (err) {{
                const textarea = document.createElement('textarea');
                textarea.value = "{safe_example}";
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                btn.innerHTML = '⚠️ 已复制';
                setTimeout(() => {{ btn.innerHTML = original; }}, 1500);
            }}
        }};
        </script>
        """, unsafe_allow_html=True)

# ===== 全局 CSS 样式 =====
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