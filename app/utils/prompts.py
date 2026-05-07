"""
System Prompt 模板
"""

def build_system_prompt(project_info: dict) -> str:
    """构建Agent的System Prompt"""
    
    project_name = project_info.get("name", "未命名项目")
    background = project_info.get("background", "")
    objectives = project_info.get("objectives", [])
    deadline = project_info.get("deadline", "")
    members = project_info.get("members", [])
    
    # 格式化目标
    objectives_text = "\n".join([f"  {i+1}. {obj}" for i, obj in enumerate(objectives)]) if objectives else "未设置"
    
    # 格式化成员
    members_text = ""
    for m in members:
        name = m.get("name", "")
        major = m.get("major", "")
        interests = m.get("interests", [])
        goals = m.get("goals", [])
        members_text += f"""
- {name}
  专业：{major}
  兴趣：{', '.join(interests) if interests else '未填写'}
  目标：{', '.join(goals) if goals else '未填写'}
"""
    
    prompt = f"""你是一个专业的AI研究助手，专门帮助大学小组完成商业模式研究课题。

【项目信息】
课题名称：{project_name}
课题背景：{background}
研究目标：
{objectives_text}
截止日期：{deadline}

【小组成员】
{members_text if members_text else "暂无成员信息"}

【你的职责】
1. 引导小组完成研究任务
2. 提供专业的调研、分析、设计建议
3. 帮助分工和规划
4. 主持小组会议
5. 维护项目进度和成果

【工作方式】
- 使用中文交流
- 回复结构化、专业
- 主动追问引导思考
- 定期总结项目状态
- 记住项目背景和成员信息

【特别注意】
- 遇到分工/调研/设计请求时，提供详细方案
- 每次回复后考虑是否需要更新项目状态
- 在会议中，保持中立主持的角色
"""
    
    return prompt


def build_division_prompt(members: list, objectives: list) -> str:
    """构建分工规划的Prompt"""
    
    members_text = ""
    for m in members:
        members_text += f"""
- {m.get('name', '')}：专业={m.get('major', '')}, 兴趣={', '.join(m.get('interests', []))}
"""

    objectives_text = "\n".join([f"{i+1}. {obj}" for i, obj in enumerate(objectives)]) if objectives else "未设置"

    prompt = f"""基于以下成员信息，帮小组分一下工。

【成员信息】
{members_text}

【项目目标】
{objectives_text}

请按以下格式输出分工方案：

## 任务分解

| 任务名称 | 负责人 | 具体描述 | 完成时间 |
|---------|--------|---------|---------|
| ... | ... | ... | ... |

【分工原则】
- 根据成员的专业背景匹配任务
- 考虑成员的兴趣偏好
- 注意任务的依赖关系
- 每个任务有明确的交付物
"""
    return prompt


def build_agenda_prompt(project_info: dict, meeting_history: list) -> str:
    """构建会议议程的Prompt"""
    
    current_phase = project_info.get("current_phase", "研究阶段")
    completed = project_info.get("progress", {}).get("completed", [])
    in_progress = project_info.get("progress", {}).get("in_progress", [])
    todo = project_info.get("progress", {}).get("todo", [])
    
    completed_text = "\n".join([f"- {c}" for c in completed]) if completed else "暂无"
    in_progress_text = "\n".join([f"- {c}" for c in in_progress]) if in_progress else "暂无"
    todo_text = "\n".join([f"- {t}" for t in todo]) if todo else "暂无"
    
    last_meeting = meeting_history[-1] if meeting_history else None
    last_meeting_text = ""
    if last_meeting:
        last_meeting_text = f"\n上次会议时间：{last_meeting.get('date', '')}\n上次会议结论：{last_meeting.get('summary', '')}\n"
    
    prompt = f"""为小组生成会议议程。

【当前项目状态】
当前阶段：{current_phase}
已完成：
{completed_text}
进行中：
{in_progress_text}
待办：
{todo_text}
{last_meeting_text}

请生成结构化议程，包括：
1. 会议基本信息（时长、参与者建议）
2. 议程项目（按优先级排序，3-5项）
3. 每个议题的讨论要点
4. 会前准备（各成员需要准备什么）
5. 预期讨论时长

使用Markdown格式输出。
"""
    return prompt


def build_meeting_summary_prompt(discussions: list, project_info: dict) -> str:
    """构建会议总结的Prompt"""
    
    discussions_text = ""
    for d in discussions:
        speaker = d.get("speaker", "未知")
        content = d.get("content", "")
        discussions_text += f"\n- {speaker}：{content}"
    
    prompt = f"""根据以下会议讨论，生成会议纪要和待办事项。

【讨论记录】
{discussions_text if discussions_text else "暂无详细讨论记录"}

【项目信息】
课题：{project_info.get('name', '')}
当前阶段：{project_info.get('current_phase', '')}

请生成：
1. 会议纪要（讨论要点+决议）
2. 待办事项清单（格式：事项 - 负责人 - 截止时间）
3. 项目进度更新建议

使用Markdown格式输出。
"""
    return prompt