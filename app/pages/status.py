"""
项目状态页面
"""
import streamlit as st
from ..utils.agent import ProjectAgent

def show():
    st.header("📊 项目状态")
    
    # 检查是否有项目
    if "project_id" not in st.session_state or not st.session_state.get("project_created"):
        st.warning("⚠️ 请先创建项目")
        if st.button("去创建项目"):
            st.session_state["page"] = "📝 初始化"
            st.rerun()
        return
    
    project_id = st.session_state["project_id"]
    project_name = st.session_state.get("project_name", "项目")
    
    # 初始化Agent获取最新数据
    if "agent" not in st.session_state:
        st.session_state["agent"] = ProjectAgent(project_id)
    
    agent = st.session_state["agent"]
    project_info = agent.get_project_info()
    
    # 项目概览
    st.markdown(f"### 📋 {project_name}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("当前阶段", project_info.get("current_phase", "研究阶段"))
    
    with col2:
        members = project_info.get("members", [])
        st.metric("小组成员", len(members))
    
    with col3:
        completed = project_info.get("progress", {}).get("completed", [])
        st.metric("已完成", len(completed))
    
    with col4:
        deadline = project_info.get("deadline", "未设置")
        st.metric("截止日期", deadline)
    
    st.markdown("---")
    
    # 课题信息
    with st.expander("📝 课题信息", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**课题背景**")
            st.markdown(project_info.get("background", "_暂无_") or "_暂无_")
            
            st.markdown("**研究目标**")
            objectives = project_info.get("objectives", [])
            if objectives:
                for obj in objectives:
                    st.markdown(f"- {obj}")
            else:
                st.markdown("_暂无_")
        
        with col2:
            st.markdown("**基本信息**")
            st.markdown(f"- 课题：{project_name}")
            st.markdown(f"- 截止：{deadline}")
            st.markdown(f"- 阶段：{project_info.get('current_phase', '研究阶段')}")
    
    # 成员信息
    with st.expander("👥 小组成员", expanded=True):
        if members:
            for m in members:
                with st.container():
                    col1, col2, col3 = st.columns([1, 2, 2])
                    
                    with col1:
                        st.markdown(f"**{m.get('name', '未知')}**")
                        st.caption(m.get('major', ''))
                    
                    with col2:
                        interests = m.get('interests', [])
                        if interests:
                            st.markdown(f"兴趣：{', '.join(interests)}")
                    
                    with col3:
                        goals = m.get('goals', [])
                        if goals:
                            st.markdown(f"目标：{', '.join(goals)}")
                    
                    st.markdown("---")
        else:
            st.info("暂无成员信息")
    
    # 进度追踪
    st.markdown("### 📈 进度追踪")
    
    progress = project_info.get("progress", {})
    completed = progress.get("completed", [])
    in_progress = progress.get("in_progress", [])
    todo = progress.get("todo", [])
    
    # 进度条
    total = len(completed) + len(in_progress) + len(todo)
    if total > 0:
        progress_pct = len(completed) / total * 100
        st.progress(progress_pct / 100, text=f"完成度：{progress_pct:.0f}%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ 已完成")
        if completed:
            for item in completed:
                st.success(f"✓ {item}")
        else:
            st.info("暂无已完成事项")
        
        st.markdown("#### 🔄 进行中")
        if in_progress:
            for item in in_progress:
                st.info(f"⟳ {item}")
        else:
            st.info("暂无进行中事项")
    
    with col2:
        st.markdown("#### 📋 待办")
        if todo:
            for item in todo:
                st.markdown(f"• {item}")
        else:
            st.info("暂无待办事项")
        
        # 阶段选择
        st.markdown("#### 🔄 更新阶段")
        phases = ["选题阶段", "调研阶段", "设计阶段", "验证阶段", "汇报阶段"]
        current_phase = project_info.get("current_phase", "调研阶段")
        
        new_phase = st.selectbox("选择当前阶段", phases, index=phases.index(current_phase) if current_phase in phases else 1)
        
        if st.button("更新阶段") and new_phase != current_phase:
            agent.memory.update_phase(new_phase)
            st.success(f"已更新为：{new_phase}")
            st.rerun()
    
    # 会议记录
    st.markdown("### 📅 会议记录")
    
    meetings = project_info.get("meetings", [])
    if meetings:
        for i, meeting in enumerate(reversed(meetings[-5:])):
            with st.expander(f"会议 {len(meetings) - i}"):
                st.markdown(f"**日期**：{meeting.get('date', '未知')}")
                st.markdown(f"**纪要**：{meeting.get('summary', '暂无')[:200]}...")
                
                discussions = meeting.get('discussions', [])
                if discussions:
                    st.markdown(f"**发言次数**：{len(discussions)}")
    else:
        st.info("暂无会议记录")
    
    # 成果积累
    st.markdown("### 🏆 已有成果")
    
    achievements = project_info.get("achievements", [])
    if achievements:
        for ach in achievements:
            st.markdown(f"- {ach}")
    else:
        st.info("暂无成果记录")
        st.markdown("在对话中提到完成的内容，AI会自动记录到这里")
    
    # 最后更新时间
    st.markdown("---")
    st.caption(f"最后更新：{project_info.get('last_updated', '未知')}")