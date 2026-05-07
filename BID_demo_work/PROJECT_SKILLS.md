# BID_demo Skills 指南

> 最后更新：2026-05-07
> 版本：V1.0

---

## 一、项目Skills概述

本文档记录了BID_demo项目的开发技能、设计决策和实现指南，供后续开发参考。

---

## 二、技术Skills

### 2.1 技术栈选择

| 技能 | 选择 | 原因 |
|------|------|------|
| 前端框架 | Streamlit | Python原生，快速开发，3天可出Demo |
| 后端服务 | FastAPI | 轻量API，异步支持 |
| 数据库 | SQLite + JSON | 免部署，Demo够用 |
| LLM | OpenAI GPT-4o | 成熟稳定，Demo主力 |

### 2.2 项目结构Skill

```
bid_demo/
├── app/
│   ├── main.py              # Streamlit入口
│   ├── pages/               # 多页面
│   │   ├── 1_初始化.py
│   │   ├── 2_对话.py
│   │   ├── 3_会议引导.py
│   │   └── 4_项目状态.py
│   ├── components/          # 可复用组件
│   └── utils/               # 工具函数
│       ├── agent.py         # Agent核心
│       ├── memory.py        # Memory管理
│       ├── prompts.py       # Prompt模板
│       └── openai_client.py # API封装
├── data/projects/           # 项目数据(JSON)
├── .env                     # 环境变量
└── requirements.txt
```

### 2.3 Agent实现Skill

**核心逻辑**：Intent识别 → Skills路由 → 执行 → Memory更新

```python
class ProjectAgent:
    def __init__(self, project_id):
        self.memory = MemoryManager(project_id)
        self.system_prompt = self._build_prompt()
    
    def chat(self, message: str) -> str:
        intent = self._recognize_intent(message)
        
        if intent == "division":
            return self._handle_division()
        elif intent == "research":
            return self._handle_research()
        # ... 其他Skills
        
        return self._default_response(message)
```

### 2.4 Intent识别Skill

| Intent | 关键词 | 触发Skill |
|--------|--------|-----------|
| division | "分工"、"分一下" | 分工规划 |
| research | "调研"、"市场" | 调研助手 |
| meeting | "开会"、"会议" | 会议主持 |
| progress | "进度"、"状态" | 进度追踪 |
| design | "设计"、"方案" | 产品设计 |
| report | "汇报"、"PPT" | 汇报准备 |

### 2.5 Memory管理Skill

**更新策略**：
- 用户请求分工 → 更新分工安排
- 会议结束 → 更新会议记录+进度
- 用户说"完成了" → 更新progress.completed
- 每10轮对话 → 自动总结更新

**数据结构**：
```json
{
  "project_id": "...",
  "name": "课题名称",
  "background": "...",
  "members": [...],
  "current_phase": "research",
  "progress": {
    "completed": [...],
    "in_progress": [...],
    "todo": [...]
  },
  "meetings": [...],
  "achievements": [...]
}
```

---

## 三、产品Skills

### 3.1 初始化流程Skill

```
Step 1: 用户输入课题信息
        - 课题名称
        - 课题背景
        - 研究目标
        - 截止日期

Step 2: 用户输入成员信息
        - 姓名
        - 专业
        - 兴趣偏好
        - 想获得的成长

Step 3: Agent生成
        - 专属人设（System Prompt）
        - 初始研究计划建议
        - 项目记忆文档框架
```

### 3.2 会议引导Skill

**三阶段流程**：
```
会前准备：
  → 根据当前进度生成议程
  → 列出需要讨论的问题
  → 分配发言角色

会中主持：
  → 记录讨论要点
  → 实时反馈和追问
  → 维持讨论方向

会后总结：
  → 生成会议纪要
  → 提取待办事项
  → 更新项目进度
```

### 3.3 角色分配Skill

根据成员特点分配讨论角色：
| 角色 | 职责 | 适合特点 |
|------|------|----------|
| 分析者 | 拆解问题、评估方案 | 逻辑思维强 |
| 表达者 | 总结归纳、汇报 | 口头表达好 |
| 调研者 | 信息搜集、数据 | 信息检索强 |
| 质疑者 | 提出反对、完善 | 批判性思维 |

### 3.4 发言辅助Skill

提供结构化模板："结论-论据-案例"

```markdown
【结论】我认为是...
【论据】原因是：
  1. ...
  2. ...
【案例】比如...
```

---

## 四、部署Skills

### 4.1 Streamlit Cloud部署

1. 代码推送到GitHub
2. 访问 https://share.streamlit.io
3. New app → 选择仓库 → Deploy
4. Settings中添加 `OPENAI_API_KEY`

### 4.2 环境变量

```bash
# .env文件
OPENAI_API_KEY=sk-xxxxx
```

---

## 五、设计决策Skills

### 5.1 为什么选择Streamlit自研？

| 因素 | Streamlit自研 | Dify平台 |
|------|--------------|----------|
| 开发控制 | 完全掌控 | 受限于平台 |
| 调试效率 | 本地直调 | 需配置部署 |
| 3天时间 | 足够 | 紧张 |
| 后续扩展 | 预留Dify路径 | - |

**决策**：短期Streamlit快速验证，长期Dify扩展

### 5.2 为什么先做单Agent？

- 3天时间有限
- 单Agent + Skills路由已能满足Demo需求
- 多Agent协作放到V2.0

### 5.3 为什么三层记忆架构？

- 支持未来多用户系统
- 教师端需要汇总所有小组
- 个人成长需要独立追踪

---

## 六、演示Skills

### 6.1 演示流程（约10分钟）

```
1. 打开应用（1分钟）
2. 演示初始化：输入课题+成员（3分钟）
3. 演示对话：触发分工规划（2分钟）
4. 演示会议：生成议程（2分钟）
5. 演示Memory：查看项目状态（2分钟）
```

### 6.2 演示数据

```python
DEMO_PROJECT = {
    "name": "新能源汽车校园共享充电桩",
    "background": "随着新能源汽车普及...",
    "members": [
        {"name": "李明", "major": "计算机", "interests": ["产品设计"]},
        {"name": "王芳", "major": "市场营销", "interests": ["品牌推广"]},
        {"name": "张强", "major": "金融学", "interests": ["财务分析"]},
        {"name": "陈静", "major": "工业设计", "interests": ["UI设计"]}
    ],
    "deadline": "2026-06-15"
}
```

---

## 七、升级路线Skill

| 版本 | 升级内容 | 技术 |
|------|----------|------|
| V1.0 | Demo基础功能 | Streamlit单Agent |
| V1.5 | 用户系统+多小组隔离 | +用户认证 |
| V2.0 | 多Agent协作 | Dify + CrewAI |
| V2.5 | 高级Memory | Mem0/Letta |
| V3.0 | 完整功能 | 全部集成 |

---

## 八、参考资源

### 8.1 开源项目参考
| 项目 | 用途 |
|------|------|
| Dify | 多Agent编排（V2.0） |
| CrewAI | 多角色Agent协作 |
| Mem0 | 通用记忆层 |
| LangGraph | 复杂工作流 |

### 8.2 API文档
- OpenAI: https://platform.openai.com/docs
- Streamlit: https://docs.streamlit.io

---

*Skills版本：V1.0*
*开发时参考此文件*