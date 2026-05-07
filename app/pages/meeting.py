"""
会议引导页面
"""
import streamlit as st
from datetime import datetime
from ..utils.agent import ProjectAgent

def show():
    st.header("📅 会议引导")
    
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
    
    # 会议状态管理
    if "meeting_active" not in st.session_state:
        st.session_state["meeting_active"] = False
    if "discussions" not in st.session_state:
        st.session_state["discussions"] = []
    
    # 根据状态显示不同内容
    if not st.session_state["meeting_active"]:
        # 会议准备阶段
        show_pre_meeting(agent, project_info, project_name)
    else:
        # 会议进行中
        show_in_meeting(agent, project_info)

def show_pre_meeting(agent, project_info, project_name):
    """会议准备阶段"""
    
    st.markdown(f"""
    ### 🎯 会议准备
    
    **项目**：{project_name}
    **当前阶段**：{project_info.get('current_phase', '研究阶段')}
    """)
    
    # 显示当前进度
    col1, col2, col3 = st.columns(3)
    
    with col1:
        completed = project_info.get("progress", {}).get("completed", [])
        st.metric("已完成", len(completed))
    
    with col2:
        in_progress = project_info.get("progress", {}).get("in_progress", [])
        st.metric("进行中", len(in_progress))
    
    with col3:
        todo = project_info.get("progress", {}).get("todo", [])
        st.metric("待办", len(todo))
    
    st.markdown("---")
    
    # 会议选项
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 生成会议议程")
        st.markdown("让AI根据当前项目状态，生成一个讨论议程")
        
        if st.button("✨ 生成议程", type="primary", use_container_width=True):
            with st.spinner("生成中..."):
                try:
                    agenda = agent._handle_agenda()
                    st.session_state["generated_agenda"] = agenda
                except Exception as e:
                    st.error(f"生成失败：{str(e)}")
    
    with col2:
        st.markdown("### 🚀 直接开始会议")
        st.markdown("跳过议程，直接开始自由讨论")
        
        if st.button("▶️ 开始会议", type="primary", use_container_width=True):
            st.session_state["meeting_active"] = True
            st.session_state["discussions"] = []
            st.rerun()
    
    # 显示生成的议程
    if "generated_agenda" in st.session_state:
        st.markdown("---")
        st.markdown("### 📝 生成的议程")
        st.markdown(st.session_state["generated_agenda"])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ 确认议程，开始会议", type="primary", use_container_width=True):
                st.session_state["meeting_active"] = True
                st.session_state["discussions"] = []
                st.rerun()
        with col2:
            if st.button("🔄 重新生成"):
                del st.session_state["generated_agenda"]
                st.rerun()

def show_in_meeting(agent, project_info):
    """会议进行中"""
    
    st.markdown("### 🔴 会议进行中...")
    
    # 会议控制
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⏹️ 结束会议", type="secondary", use_container_width=True):
            st.session_state["meeting_active"] = False
            st.rerun()
    
    with col2:
        if st.button("🔄 重置会议", type="secondary", use_container_width=True):
            st.session_state["discussions"] = []
            st.rerun()
    
    with col3:
        st.markdown(f"发言次数：{len(st.session_state['discussions'])}")
    
    st.markdown("---")
    
    # 显示议程（如果有）
    if "generated_agenda" in st.session_state:
        with st.expander("📋 查看议程"):
            st.markdown(st.session_state["generated_agenda"])
    
    # 发言记录
    st.markdown("### 💬 发言记录")
    
    if not st.session_state["discussions"]:
        st.info("暂无发言记录，开始讨论吧！")
    
    for i, disc in enumerate(st.session_state["discussions"]):
        with st.container():
            st.markdown(f"**{disc.get('speaker', '发言者')}**：{disc.get('content', '')}")
            st.caption(f"时间：{disc.get('timestamp', '')}")
            st.markdown("---")
    
    st.markdown("### ✍️ 添加发言")
    
    # 发言人输入
    col1, col2 = st.columns([3, 1])
    
    with col1:
        new发言 = st.text_input(
            "输入发言内容",
            placeholder="输入你的发言...",
            key="new_speech_input"
        )
    
    with col2:
        speaker_name = st.selectbox(
            "发言人",
            [m.get("name", "未知") for m in project_info.get("members", [])] + ["其他"]
        )
    
    if st.button("📝 记录发言", type="primary"):
        if new发言:
            st.session_state["discussions"].append({
                "speaker": speaker_name,
                "content": new发言,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()
    
    st.markdown("---")
    
    # AI辅助
    st.markdown("### 🤖 AI辅助")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💡 请AI补充观点"):
            st.session_state["ai_help_topic"] = "补充"
    
    with col2:
        if st.button("❓ 请AI提问"):
            st.session_state["ai_help_topic"] = "提问"
    
    # 会议结束处理
    st.markdown("---")
    st.markdown("### 📊 会议结束")
    
    if st.button("📝 生成会议纪要并结束", type="primary", use_container_width=True):
        with st.spinner("生成会议纪要..."):
            try:
                summary = agent.generate_meeting_summary(st.session_state["discussions"])
                
                st.session_state["meeting_summary"] = summary
                st.session_state["meeting_active"] = False
                
                st.success("会议纪要已生成！")
                st.markdown(summary)
                
                # 清空会议相关状态
                if "generated_agenda" in st.session_state:
                    del st.session_state["generated_agenda"]
                
                st.rerun()
            except Exception as e:
                st.error(f"生成失败：{str(e)}")
    
    # 显示会议纪要
    if "meeting_summary" in st.session_state and not st.session_state["meeting_active"]:
        st.markdown("---")
        st.markdown("### 📝 会议纪要")
        st.markdown(st.session_state["meeting_summary"])