"""
首页 - 项目选择
"""
import streamlit as st
from utils.memory import get_project_list
import os

def show():
    st.header("🏠 欢迎使用 GroupMind")
    
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
        st.markdown("### 📁 项目列表")
        
        # 获取项目列表
        projects = get_project_list()
        
        if projects:
            st.success(f"已有 {len(projects)} 个项目")
            for p in projects:
                project_id = p['id']
                project_name = p['name']
                is_current = st.session_state.get("project_id") == project_id
                
                # 显示项目卡片
                with st.container():
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        label = f"**{project_name}**"
                        if is_current:
                            label += " ✅"
                        
                        if st.button(label, key=f"select_{project_id}", use_container_width=True):
                            # 切换到该项目
                            st.session_state["project_id"] = project_id
                            st.session_state["project_created"] = True
                            st.session_state["project_name"] = project_name
                            st.query_params["project_id"] = project_id
                            st.rerun()
                    
                    with col_b:
                        # 删除按钮
                        if st.button("🗑️", key=f"del_{project_id}", help="删除项目"):
                            st.session_state["confirm_delete"] = project_id
                            st.session_state["delete_name"] = project_name
                            st.rerun()
                
                st.markdown("---")
        else:
            st.info("暂无项目")
        
        # 删除确认弹窗
        if st.session_state.get("confirm_delete"):
            st.error(f"⚠️ 确定要删除项目「{st.session_state.get('delete_name')}」吗？此操作不可恢复！")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("✅ 确认删除", type="primary"):
                    # 删除项目文件
                    from utils.memory import DATA_DIR
                    project_file = os.path.join(DATA_DIR, f"{st.session_state['confirm_delete']}.json")
                    if os.path.exists(project_file):
                        os.remove(project_file)
                    
                    # 如果删除的是当前项目，清除状态
                    if st.session_state.get("project_id") == st.session_state['confirm_delete']:
                        for key in ["project_id", "project_created", "project_name", "agent", "messages"]:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.query_params.clear()
                    
                    st.success("项目已删除！")
                    del st.session_state["confirm_delete"]
                    del st.session_state["delete_name"]
                    st.rerun()
            
            with col_no:
                if st.button("❌ 取消"):
                    del st.session_state["confirm_delete"]
                    del st.session_state["delete_name"]
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 🚀 快速开始")
        
        if st.button("➕ 创建新项目", type="primary", use_container_width=True):
            # 清除当前项目状态
            for key in ["project_id", "project_created", "project_name", "agent", "messages"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.query_params.clear()
            st.rerun()