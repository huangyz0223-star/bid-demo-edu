"""
对话页面 - 与Agent交互
"""
import streamlit as st
from utils.agent import ProjectAgent
from datetime import datetime

def show():
    st.header("💬 与AI助手对话")
    
    # 检查是否有项目
    if "project_id" not in st.session_state or not st.session_state.get("project_created"):
        st.warning("⚠️ 请先创建项目")
        if st.button("去创建项目"):
            st.session_state["page"] = "📝 初始化"
            st.rerun()
        return
    
    project_id = st.session_state["project_id"]
    project_name = st.session_state.get("project_name", "项目")
    
    # 初始化Agent
    if "agent" not in st.session_state:
        st.session_state["agent"] = ProjectAgent(project_id)
    
    agent = st.session_state["agent"]
    project_info = agent.get_project_info()
    
    # 侧边栏显示项目信息
    with st.sidebar:
        st.markdown("### 📋 当前项目")
        st.markdown(f"**{project_name}**")
        st.markdown(f"阶段：{project_info.get('current_phase', '研究阶段')}")
        st.markdown("---")
        
        # 快捷指令
        st.markdown("### ⚡ 快捷指令")
        
        quick_actions = [
            "帮我们分一下工",
            "开个会讨论一下",
            "看看项目进度",
            "调研一下市场",
            "准备汇报材料"
        ]
        
        for action in quick_actions:
            if st.button(action, use_container_width=True):
                # 模拟用户输入
                st.session_state["quick_input"] = action
        
        st.markdown("---")
        st.markdown("### 📊 统计")
        st.markdown(f"- 对话轮次：{len(project_info.get('conversations', [])) // 2}")
        st.markdown(f"- 会议次数：{len(project_info.get('meetings', []))}")
    
    # 显示对话历史
    st.markdown("### 💬 对话记录")
    
    # 初始化消息历史
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        
        # 添加欢迎消息
        welcome_msg = f"""你好！我是你的AI研究助手。

**项目**：{project_name}
**当前阶段**：{project_info.get('current_phase', '研究阶段')}

我可以帮你：
- 📊 调研和分析
- 📝 分工和规划
- 📅 组织和主持会议
- 📋 跟踪项目进度

有什么需要帮助的吗？"""
        
        st.session_state["messages"].append({
            "role": "assistant",
            "content": welcome_msg
        })
    
    # 显示消息
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])
    
    # 检查是否有快捷输入
    default_input = st.session_state.pop("quick_input", "")
    
    # 输入框（兼容旧版本Streamlit）
    st.markdown("---")
    user_input = st.text_input("输入你的问题：", key="chat_input")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        send_button = st.button("发送", type="primary")
    with col2:
        if st.button("🗑️ 清空对话"):
            st.session_state["messages"] = []
            st.rerun()
    
    if (user_input or default_input) and send_button:
        input_text = user_input or default_input
        
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(input_text)
        
        st.session_state["messages"].append({
            "role": "user",
            "content": input_text
        })
        
        # 调用Agent
        with st.spinner("思考中..."):
            try:
                response, intent = agent.chat(input_text)
            except Exception as e:
                response = f"抱歉，发生了错误：{str(e)}"
                intent = "error"
        
        # 显示AI响应
        with st.chat_message("assistant"):
            st.markdown(response)
            
            # 根据意图显示提示
            if intent == "division":
                st.info("💡 已触发分工规划Skill")
            elif intent == "meeting":
                st.info("💡 已进入会议模式")
            elif intent == "progress":
                st.info("💡 已查询项目状态")
        
        st.session_state["messages"].append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()