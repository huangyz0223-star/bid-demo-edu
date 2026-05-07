"""
Streamlit应用入口
"""
import streamlit as st
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 页面配置
st.set_page_config(
    page_title="BID_demo - 小组研究Agent",
    page_icon="🎓",
    layout="wide"
)

# 页面标题
st.title("🎓 BID_demo - 商业模式教学小组研究Agent")
st.markdown("---")

# 从URL参数获取项目ID
query_params = st.query_params
url_project_id = query_params.get("project_id", None)

# 如果URL有项目ID，同步到session_state
if url_project_id:
    st.session_state["project_id"] = url_project_id
    st.session_state["project_created"] = True

# 侧边栏导航
st.sidebar.title("导航")

# 根据是否有项目来显示不同选项
if st.session_state.get("project_created"):
    options = ["🏠 首页", "💬 对话", "📅 会议", "📊 状态"]
    default_index = 1  # 默认选中对话
else:
    options = ["🏠 首页", "📝 初始化"]
    default_index = 1

page = st.sidebar.radio(
    "选择功能",
    options,
    index=default_index
)

# 直接导入页面模块
if page == "🏠 首页":
    from pages import home
    home.show()
elif page == "📝 初始化":
    from pages import init
    init.show()
elif page == "💬 对话":
    from pages import chat
    chat.show()
elif page == "📅 会议":
    from pages import meeting
    meeting.show()
elif page == "📊 状态":
    from pages import status
    status.show()