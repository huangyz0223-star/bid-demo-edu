"""
Memory 管理器 - 维护项目的记忆状态
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "projects")

class MemoryManager:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.file_path = os.path.join(DATA_DIR, f"{project_id}.json")
        self._ensure_data_dir()
        self.data = self._load()
    
    def _ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def _load(self) -> Dict[str, Any]:
        """加载记忆数据"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        # 返回默认结构
        return {
            "project_id": self.project_id,
            "name": "",
            "background": "",
            "objectives": [],
            "members": [],
            "deadline": "",
            "current_phase": "研究阶段",
            "progress": {
                "completed": [],
                "in_progress": [],
                "todo": []
            },
            "achievements": [],
            "meetings": [],
            "conversations": [],
            "last_updated": datetime.now().isoformat()
        }
    
    def save(self):
        """保存记忆数据"""
        self.data["last_updated"] = datetime.now().isoformat()
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def update_project_info(self, name: str, background: str, objectives: list, deadline: str):
        """更新项目基本信息"""
        self.data["name"] = name
        self.data["background"] = background
        self.data["objectives"] = objectives if isinstance(objectives, list) else [objectives]
        self.data["deadline"] = deadline
        self.save()
    
    def update_members(self, members: list):
        """更新成员信息"""
        self.data["members"] = members
        self.save()
    
    def update_progress(self, completed: list = None, in_progress: list = None, todo: list = None):
        """更新进度"""
        if completed is not None:
            self.data["progress"]["completed"] = completed
        if in_progress is not None:
            self.data["progress"]["in_progress"] = in_progress
        if todo is not None:
            self.data["progress"]["todo"] = todo
        self.save()
    
    def update_phase(self, phase: str):
        """更新当前阶段"""
        self.data["current_phase"] = phase
        self.save()
    
    def add_conversation(self, role: str, content: str):
        """添加对话记录"""
        self.data["conversations"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        # 只保留最近50条对话
        if len(self.data["conversations"]) > 50:
            self.data["conversations"] = self.data["conversations"][-50:]
        self.save()
    
    def add_meeting(self, meeting_data: dict):
        """添加会议记录"""
        self.data["meetings"].append(meeting_data)
        self.save()
    
    def add_achievement(self, achievement: str):
        """添加成果"""
        if achievement not in self.data["achievements"]:
            self.data["achievements"].append(achievement)
            self.save()
    
    def get_summary(self) -> str:
        """获取项目摘要"""
        return f"""
【项目】{self.data['name']}
【阶段】{self.data['current_phase']}
【进度】已完成 {len(self.data['progress']['completed'])} 项，进行中 {len(self.data['progress']['in_progress'])} 项，待办 {len(self.data['progress']['todo'])} 项
【成员】{len(self.data['members'])} 人
【截止】{self.data['deadline']}
"""
    
    def get_full_info(self) -> Dict[str, Any]:
        """获取完整项目信息"""
        return self.data.copy()


def get_project_list() -> list:
    """获取所有项目列表"""
    os.makedirs(DATA_DIR, exist_ok=True)
    projects = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            project_id = filename[:-5]
            file_path = os.path.join(DATA_DIR, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    projects.append({
                        "id": project_id,
                        "name": data.get("name", "未命名"),
                        "current_phase": data.get("current_phase", ""),
                        "last_updated": data.get("last_updated", "")
                    })
            except:
                pass
    return projects