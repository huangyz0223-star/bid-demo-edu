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
    # 加载项目名称
    from utils.memory import MemoryManager
    memory = MemoryManager(url_project_id)
    project_info = memory.get_full_info()
    st.session_state["project_name"] = project_info.get("name", "已有项目")

# 侧边栏导航
st.sidebar.title("📌 导航")
page = st.sidebar.radio(
    "选择页面",
    ["🏠 首页", "💬 对话", "📅 会议", "📊 状态"]
)

# 直接导入页面模块
if page == "🏠 首页":
    from pages import home
    home.show()
elif page == "💬 对话":
    from pages import chat
    chat.show()
elif page == "📅 会议":
    from pages import meeting
    meeting.show()
elif page == "📊 状态":
    from pages import status
    status.show()