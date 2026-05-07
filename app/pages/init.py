"""
初始化页面 - 创建新项目
"""
import streamlit as st
from datetime import datetime
from utils.memory import MemoryManager

def show():
    st.header("📝 创建新项目")
    
    # 检查是否已有项目ID
    if "project_id" not in st.session_state:
        st.session_state["project_id"] = f"project_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    project_id = st.session_state["project_id"]
    
    st.info(f"项目ID: {project_id}")
    
    # 项目信息表单
    st.markdown("### 📋 项目信息")
    
    with st.form("project_form"):
        project_name = st.text_input(
            "课题名称",
            placeholder="例如：新能源汽车校园共享充电桩",
            help="输入你们小组的研究课题"
        )
        
        project_background = st.text_area(
            "课题背景",
            placeholder="描述课题的背景和意义...",
            height=100,
            help="简要描述为什么选择这个课题"
        )
        
        project_objectives = st.text_area(
            "研究目标",
            placeholder="1. 完成市场调研\n2. 设计产品方案\n3. 准备汇报展示",
            height=100,
            help="列出研究的主要目标，每行一个"
        )
        
        project_deadline = st.date_input(
            "截止日期",
            value=datetime.now().replace(month=datetime.now().month + 1),
            help="项目截止日期"
        )
        
        st.markdown("---")
        st.markdown("### 👥 小组成员")
        
        # 成员数量
        num_members = st.number_input("小组成员数量", min_value=1, max_value=10, value=3)
        
        members = []
        for i in range(num_members):
            st.markdown(f"**成员 {i+1}**")
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(f"姓名", key=f"name_{i}", placeholder="输入姓名")
                major = st.text_input(f"专业", key=f"major_{i}", placeholder="例如：计算机、金融")
            
            with col2:
                interests = st.text_input(f"兴趣偏好", key=f"interests_{i}", placeholder="例如：产品设计、数据分析")
                goals = st.text_input(f"想获得的成长", key=f"goals_{i}", placeholder="例如：提升表达能力")
            
            if name:
                members.append({
                    "name": name,
                    "major": major,
                    "interests": [x.strip() for x in interests.split(",") if x.strip()],
                    "goals": [x.strip() for x in goals.split(",") if x.strip()]
                })
            
            st.markdown("---")
        
        submitted = st.form_submit_button("🚀 创建项目", type="primary", use_container_width=True)
        
        if submitted:
            if not project_name:
                st.error("请输入课题名称")
            elif not members:
                st.error("请至少添加一名成员")
            else:
                # 保存项目信息
                memory = MemoryManager(project_id)
                memory.update_project_info(
                    name=project_name,
                    background=project_background,
                    objectives=[x.strip() for x in project_objectives.split("\n") if x.strip()],
                    deadline=str(project_deadline)
                )
                memory.update_members(members)
                
                # 设置session state
                st.session_state["project_created"] = True
                st.session_state["project_name"] = project_name
                
                st.success("✅ 项目创建成功！")
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💬 开始对话", type="primary", use_container_width=True):
                        st.session_state["page"] = "💬 对话"
                        st.rerun()
                with col2:
                    if st.button("📊 查看状态", use_container_width=True):
                        st.session_state["page"] = "📊 状态"
                        st.rerun()