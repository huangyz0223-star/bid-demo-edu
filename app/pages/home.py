"""
首页 - 项目选择
"""
import streamlit as st
import os
from utils.memory import get_project_list

def show():
    st.header("🏠 欢迎使用 BID_demo")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 产品定位
        
        **AI Project Coach / AI Discussion Facilitator**
        
        帮助大学小组完成商业模式研究课题的AI助手。
        
        #### 核心功能
        
        | 功能 | 说明 |
        |------|------|
        | 📝 初始化 | 输入课题和成员信息 |
        | 💬 对话 | 与AI助手多轮交互 |
        | 📅 会议 | 会议引导和纪要生成 |
        | 📊 状态 | 查看项目进度和成果 |
        
        #### 快捷指令
        
        在对话中可以输入：
        - `"帮我们分一下工"` - 生成任务分配
        - `"开个会"` - 进入会议模式
        - `"看看进度"` - 查看项目状态
        - `"调研一下市场"` - 触发调研助手
        """)
    
    with col2:
        st.markdown("### 📁 选择项目")
        
        # 获取项目列表
        projects = get_project_list()
        
        if projects:
            st.success(f"已有 {len(projects)} 个项目")
            for p in projects:
                st.markdown(f"- **{p['name']}** ({p['current_phase']})")
        else:
            st.info("暂无项目，请先创建新项目")
        
        st.markdown("---")
        st.markdown("### 🚀 快速开始")
        
        if st.button("➕ 创建新项目", type="primary", use_container_width=True):
            st.session_state["page"] = "📝 初始化"
            st.rerun()