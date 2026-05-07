"""
ProjectAgent - 小组研究Agent核心类
"""
from typing import Optional, Tuple
from .memory import MemoryManager
from .openai_client import get_openai_client
from .prompts import (
    build_system_prompt, 
    build_division_prompt, 
    build_agenda_prompt,
    build_meeting_summary_prompt
)


class ProjectAgent:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.memory = MemoryManager(project_id)
        self.openai = get_openai_client()
        self.conversation_history = []
        
        # 从Memory加载对话历史
        data = self.memory.get_full_info()
        for conv in data.get("conversations", [])[-20:]:
            self.conversation_history.append({
                "role": conv["role"],
                "content": conv["content"]
            })
    
    def _build_system_prompt(self) -> str:
        """构建System Prompt"""
        project_info = self.memory.get_full_info()
        return build_system_prompt(project_info)
    
    def _recognize_intent(self, message: str) -> str:
        """识别用户意图"""
        message_lower = message.lower()
        
        # 分工相关
        if any(kw in message_lower for kw in ["分工", "分一下", "任务分配", "安排任务"]):
            return "division"
        
        # 调研相关
        if any(kw in message_lower for kw in ["调研", "了解一下", "市场", "调查", "研究一下"]):
            return "research"
        
        # 会议相关
        if any(kw in message_lower for kw in ["开会", "会议", "讨论", "研讨"]):
            if "议程" in message or "准备" in message:
                return "agenda"
            return "meeting"
        
        # 进度相关
        if any(kw in message_lower for kw in ["进度", "看看状态", "还剩什么", "完成了什么"]):
            return "progress"
        
        # 设计相关
        if any(kw in message_lower for kw in ["设计", "方案", "产品", "怎么做"]):
            return "design"
        
        # 汇报相关
        if any(kw in message_lower for kw in ["汇报", "ppt", "演讲", "展示", "准备汇报"]):
            return "report"
        
        # 完成相关
        if any(kw in message_lower for kw in ["完成了", "完成了", "搞定了", "结束了"]):
            return "complete"
        
        return "general"
    
    def chat(self, user_message: str) -> Tuple[str, str]:
        """
        处理用户消息并返回响应
        返回: (响应内容, 意图类型)
        """
        # 识别意图
        intent = self._recognize_intent(user_message)
        
        # 根据意图处理
        if intent == "division":
            response = self._handle_division()
        elif intent == "agenda":
            response = self._handle_agenda()
        elif intent == "meeting":
            response = self._handle_meeting()
        elif intent == "progress":
            response = self._handle_progress()
        elif intent == "complete":
            response = self._handle_complete(user_message)
        else:
            response = self._default_response(user_message)
        
        # 保存对话记录
        self.memory.add_conversation("user", user_message)
        self.memory.add_conversation("assistant", response)
        
        return response, intent
    
    def _default_response(self, user_message: str) -> str:
        """默认对话处理"""
        system_prompt = self._build_system_prompt()
        
        # 构建上下文
        context = ""
        if self.conversation_history[-5:]:
            context = "\n\n【最近对话】\n"
            for conv in self.conversation_history[-5:]:
                role_name = "用户" if conv["role"] == "user" else "AI"
                context += f"{role_name}：{conv['content'][:200]}...\n"
        
        full_message = f"{context}\n\n【当前消息】\n{user_message}"
        
        return self.openai.chat(system_prompt, full_message)
    
    def _handle_division(self) -> str:
        """处理分工请求"""
        data = self.memory.get_full_info()
        members = data.get("members", [])
        objectives = data.get("objectives", [])
        
        prompt = build_division_prompt(members, objectives)
        system_prompt = "你是一个专业的项目管理专家，擅长根据成员特点和项目目标进行合理的任务分配。"
        
        response = self.openai.chat(system_prompt, prompt)
        
        # 更新待办事项
        if objectives and not data.get("progress", {}).get("todo"):
            self.memory.update_progress(todo=objectives)
        
        return response
    
    def _handle_agenda(self) -> str:
        """处理议程生成请求"""
        data = self.memory.get_full_info()
        meetings = data.get("meetings", [])
        
        prompt = build_agenda_prompt(data, meetings)
        system_prompt = "你是一个专业的会议主持专家，擅长设计高效的小组讨论议程。"
        
        return self.openai.chat(system_prompt, prompt)
    
    def _handle_meeting(self) -> str:
        """处理会议请求"""
        data = self.memory.get_full_info()
        
        # 生成简短的开场
        project_name = data.get("name", "本项目")
        current_phase = data.get("current_phase", "研究阶段")
        completed = data.get("progress", {}).get("completed", [])
        
        intro = f"""好的，让我们开始一次小组讨论。

【项目】{project_name}
【当前阶段】{current_phase}
【已完成】{', '.join(completed) if completed else '暂无'}

请告诉我你们今天想要讨论什么主题？或者我可以帮你们：
1. 生成一个讨论议程
2. 回顾当前进度
3. 针对某个具体问题进行讨论
"""
        return intro
    
    def _handle_progress(self) -> str:
        """处理进度查询"""
        data = self.memory.get_full_info()
        
        project_name = data.get("name", "未命名项目")
        current_phase = data.get("current_phase", "研究阶段")
        completed = data.get("progress", {}).get("completed", [])
        in_progress = data.get("progress", {}).get("in_progress", [])
        todo = data.get("progress", {}).get("todo", [])
        deadline = data.get("deadline", "未设置")
        
        response = f"""## 【{project_name}】项目状态

### 当前阶段
{current_phase}

### 进度概览
- ✅ 已完成：{len(completed)} 项
- 🔄 进行中：{len(in_progress)} 项  
- 📋 待办：{len(todo)} 项

### 已完成事项
"""
        if completed:
            for item in completed:
                response += f"- {item}\n"
        else:
            response += "_暂无_\n"
        
        response += "\n### 进行中事项\n"
        if in_progress:
            for item in in_progress:
                response += f"- {item}\n"
        else:
            response += "_暂无_\n"
        
        response += "\n### 待办事项\n"
        if todo:
            for item in todo:
                response += f"- {item}\n"
        else:
            response += "_暂无_\n"
        
        response += f"\n### 截止日期\n{deadline}"
        
        return response
    
    def _handle_complete(self, user_message: str) -> str:
        """处理完成标记"""
        # 尝试从消息中提取完成的事项
        data = self.memory.get_full_info()
        completed = data.get("progress", {}).get("completed", [])
        in_progress = data.get("progress", {}).get("in_progress", [])
        
        # 简单的文本匹配
        for item in in_progress:
            if item.lower() in user_message.lower():
                completed.append(item)
                in_progress.remove(item)
                self.memory.update_progress(completed=completed, in_progress=in_progress)
                return f"好的，我记录下来：✅ **{item}** 已完成！\n\n目前已完成 {len(completed)} 项，还有 {len(in_progress)} 项进行中。"
        
        return "好的，已记录完成！还有什么需要帮助的吗？"
    
    def generate_meeting_summary(self, discussions: list) -> str:
        """生成会议纪要"""
        data = self.memory.get_full_info()
        prompt = build_meeting_summary_prompt(discussions, data)
        system_prompt = "你是一个专业的会议记录专家，擅长整理讨论要点、生成会议纪要和待办事项。"
        
        summary = self.openai.chat(system_prompt, prompt)
        
        # 保存会议记录
        meeting_data = {
            "date": "",
            "summary": summary[:500],
            "discussions": discussions
        }
        self.memory.add_meeting(meeting_data)
        
        return summary
    
    def get_project_info(self) -> dict:
        """获取项目信息"""
        return self.memory.get_full_info()