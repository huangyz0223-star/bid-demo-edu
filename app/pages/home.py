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
        
        **GroupMind = Group（小组）+ Mind（智能）**
        
        帮助大学小组完成商业模式研究课题的AI助手。
        
        #### 核心功能
        
        | 功能 | 说明 |
        |------|------|
        | 💬 对话 | 与AI助手多轮交互 |
        | 📅 会议 | 会议引导和纪要生成 |
        | 📊 状态 | 查看项目进度和成果 |
        
        #### 快捷指令
        
        在对话中可以输入：
        - `"帮我们分一下工"` - 生成任务分配
        - `"开个会"` - 进入会议模式
        - `"看看进度"` - 查看项目状态
        """)
    
    with col2:
        st.markdown("### 📁 我的项目")
        
        # 获取项目列表
        projects = get_project_list()
        
        if projects:
            st.success(f"已有 {len(projects)} 个项目")
            for p in projects:
                project_id = p['id']
                project_name = p['name']
                is_current = st.session_state.get("project_id") == project_id
                
                with st.container():
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        label = f"**{project_name}**"
                        if is_current:
                            label += " ✅"
                        
                        if st.button(label, key=f"select_{project_id}", use_container_width=True):
                            st.session_state["project_id"] = project_id
                            st.session_state["project_created"] = True
                            st.session_state["project_name"] = project_name
                            st.query_params["project_id"] = project_id
                            st.rerun()
                    
                    with col_b:
                        if st.button("🗑️", key=f"del_{project_id}", help="删除项目"):
                            st.session_state["confirm_delete"] = project_id
                            st.session_state["delete_name"] = project_name
                            st.rerun()
                
                st.markdown("---")
        else:
            st.info("暂无项目")
        
        # 删除确认
        if st.session_state.get("confirm_delete"):
            st.error(f"⚠️ 确定要删除「{st.session_state.get('delete_name')}」吗？")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("✅ 确认删除", type="primary"):
                    from utils.memory import DATA_DIR
                    project_file = os.path.join(DATA_DIR, f"{st.session_state['confirm_delete']}.json")
                    if os.path.exists(project_file):
                        os.remove(project_file)
                    del st.session_state["confirm_delete"]
                    del st.session_state["delete_name"]
                    st.rerun()
            with col_no:
                if st.button("❌ 取消"):
                    del st.session_state["confirm_delete"]
                    del st.session_state["delete_name"]
                    st.rerun()
        
        st.markdown("---")
        
        # 创建新项目按钮
        if st.button("➕ 创建新项目", type="primary", use_container_width=True):
            st.session_state["show_init_form"] = True
            st.rerun()
    
    # 展开的创建表单
    if st.session_state.get("show_init_form"):
        st.markdown("---")
        st.markdown("### 📝 创建新项目")
        
        with st.form("init_form"):
            # 项目基本信息
            st.markdown("#### 📋 项目信息")
            project_name = st.text_input(
                "课题名称 *",
                placeholder="例如：新能源汽车校园共享充电桩"
            )
            project_background = st.text_area(
                "课题背景",
                placeholder="描述课题的背景、意义和目标用户..."
            )
            project_objectives = st.text_area(
                "研究目标",
                placeholder="1. 完成市场调研\n2. 设计产品方案\n3. 准备汇报展示"
            )
            project_deadline = st.date_input("截止日期")
            
            st.markdown("---")
            
            # 成员信息
            st.markdown("#### 👥 小组成员")
            num_members = st.number_input("成员数量", min_value=1, max_value=10, value=3)
            
            members = []
            for i in range(num_members):
                st.markdown(f"**成员 {i+1}**")
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    name = st.text_input(f"姓名", key=f"name_{i}", placeholder="姓名")
                    major = st.text_input(f"专业", key=f"major_{i}", placeholder="专业")
                
                with col_b:
                    interests = st.text_input(f"兴趣偏好", key=f"interests_{i}", placeholder="如：产品设计、数据分析")
                    goals = st.text_input(f"想获得的成长", key=f"goals_{i}", placeholder="如：提升表达能力")
                
                with col_c:
                    mbti = st.selectbox(f"MBTI", ["", "INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"], key=f"mbti_{i}")
                    role_preference = st.text_input(f"偏好角色", key=f"role_{i}", placeholder="如：分析者、表达者")
                
                if name:
                    members.append({
                        "name": name,
                        "major": major,
                        "interests": [x.strip() for x in interests.split(",") if x.strip()],
                        "goals": [x.strip() for x in goals.split(",") if x.strip()],
                        "mbti": mbti,
                        "role_preference": role_preference
                    })
                
                st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("🚀 创建项目", type="primary", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("❌ 取消", use_container_width=True)
            
            if cancel:
                st.session_state["show_init_form"] = False
                st.rerun()
            
            if submitted:
                if not project_name:
                    st.error("请输入课题名称")
                elif not members:
                    st.error("请至少添加一名成员")
                else:
                    from datetime import datetime
                    from utils.memory import MemoryManager
                    
                    project_id = f"project_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    memory = MemoryManager(project_id)
                    memory.update_project_info(
                        name=project_name,
                        background=project_background,
                        objectives=[x.strip() for x in project_objectives.split("\n") if x.strip()],
                        deadline=str(project_deadline)
                    )
                    memory.update_members(members)
                    
                    st.session_state["project_id"] = project_id
                    st.session_state["project_created"] = True
                    st.session_state["project_name"] = project_name
                    st.session_state["show_init_form"] = False
                    st.query_params["project_id"] = project_id
                    
                    st.success("✅ 项目创建成功！")
                    st.rerun()