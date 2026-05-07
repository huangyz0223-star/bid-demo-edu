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

# 侧边栏导航
st.sidebar.title("导航")
page = st.sidebar.radio(
    "选择功能",
    ["🏠 首页", "📝 初始化", "💬 对话", "📅 会议", "📊 状态"]
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