"""
LLM统一客户端 - 支持多种API和演示模式
"""
import os
import json
from abc import ABC, abstractmethod
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ============== 抽象基类 ==============
class LLMClient(ABC):
    """LLM客户端抽象基类"""
    
    @abstractmethod
    def chat(self, system_prompt: str, user_message: str) -> str:
        """发送对话请求"""
        pass


# ============== 演示模式实现 ==============
class DemoClient(LLMClient):
    """演示模式客户端 - 不需要API Key"""
    
    def __init__(self):
        self.responses = {
            "division": """## 📋 分工方案建议

根据成员特点，建议分工如下：

| 任务 | 负责人 | 说明 |
|------|--------|------|
| 市场调研 | 张强 | 负责收集行业数据 |
| 用户研究 | 王芳 | 负责问卷和访谈 |
| 产品设计 | 李明 | 负责方案设计 |
| 财务分析 | 陈静 | 负责成本收益 |

**建议**：先完成市场调研，再进行产品设计。
""",
            "agenda": """## 📅 会议议程

**项目**：新能源汽车校园共享充电桩
**时长**：45分钟
**参与**：全体成员

### 议程

1. **进度回顾**（10分钟）
   - 上周完成事项
   - 遇到的问题

2. **议题讨论**（25分钟）
   - 议题A：目标用户定位
   - 议题B：盈利模式设计
   - 议题C：竞争优势

3. **任务分配**（5分钟）
   - 确认下周待办
   - 负责人确认

4. **其他事项**（5分钟）

---
💡 会前请准备：各自分享对目标用户的理解
""",
            "meeting": """好的，让我们开始讨论！

**当前阶段**：调研阶段
**已完成**：课题确定、初步调研
**进行中**：深度调研

请告诉我你们今天想要讨论什么？
或者我可以帮你们：
1. 回顾一下当前进度
2. 针对某个具体问题展开讨论
3. 整理一下思路
""",
            "progress": """## 📊 项目状态

**课题**：新能源汽车校园共享充电桩
**阶段**：调研阶段
**截止**：2026-06-15

### 进度

| 状态 | 数量 | 详情 |
|------|------|------|
| ✅ 已完成 | 2项 | 课题确定、初步调研 |
| 🔄 进行中 | 1项 | 深度调研 |
| 📋 待办 | 3项 | 产品设计、方案撰写、PPT制作 |

### 下一步建议
1. 完成深度调研报告
2. 召开小组会议讨论方向
3. 开始产品方案设计
""",
            "research": """## 🔍 市场调研概览

**新能源汽车市场趋势**
- 2024年新能源汽车渗透率已超过30%
- 大学生群体对新能源车兴趣度逐年上升
- 校园充电需求日益增长

**校园场景特点**
- 停车位相对固定，适合建设充电桩
- 学生消费能力有限，需要合理定价
- 可结合共享经济模式

**建议调研方向**
1. 校园内新能源汽车保有量
2. 学生购买意愿调研
3. 竞品分析（校外充电桩）
""",
            "default": """我理解你的问题。

作为你们的AI研究助手，我可以帮你：
- 📊 分析问题和提供建议
- 📝 整理思路和输出文档
- 📋 分工规划和进度跟踪
- 💬 主持会议和记录讨论

请告诉我你们现在遇到的具体问题是什么？
"""
        }
    
    def chat(self, system_prompt: str, user_message: str) -> str:
        """根据用户消息返回预设响应"""
        msg_lower = user_message.lower()
        
        # 根据关键词匹配响应
        if any(kw in msg_lower for kw in ["分工", "分一下", "任务分配"]):
            return self.responses["division"]
        elif "议程" in msg_lower or ("会议" in msg_lower and "准备" in msg_lower):
            return self.responses["agenda"]
        elif any(kw in msg_lower for kw in ["开会", "会议", "讨论"]):
            return self.responses["meeting"]
        elif any(kw in msg_lower for kw in ["进度", "看看状态", "还剩什么"]):
            return self.responses["progress"]
        elif any(kw in msg_lower for kw in ["调研", "市场", "调查"]):
            return self.responses["research"]
        else:
            return self.responses["default"]


# ============== OpenAI 实现 ==============
class OpenAIClient(LLMClient):
    """OpenAI GPT客户端"""
    
    def __init__(self, model: str = "gpt-4o"):
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("请在.env中设置 OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def chat(self, system_prompt: str, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content


# ============== 智谱GLM 实现 ==============
class ZhipuClient(LLMClient):
    """智谱GLM客户端"""
    
    def __init__(self, model: str = "glm-4"):
        api_key = os.getenv("ZHIPU_API_KEY")
        if not api_key:
            raise ValueError("请在.env中设置 ZHIPU_API_KEY")
        self.api_key = api_key
        self.model = model
        self.base_url = "https://open.bigmodel.cn/api/paas/v4"
    
    def chat(self, system_prompt: str, user_message: str) -> str:
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API请求失败: {response.status_code} - {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]


# ============== Claude 实现 ==============
class ClaudeClient(LLMClient):
    """Anthropic Claude客户端"""
    
    def __init__(self, model: str = "claude-3-sonnet-20240229"):
        import anthropic
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("请在.env中设置 ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    def chat(self, system_prompt: str, user_message: str) -> str:
        message = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return message.content[0].text


# ============== MiniMax 实现 ==============
class MiniMaxClient(LLMClient):
    """MiniMax AI客户端"""
    
    def __init__(self, model: str = "abab6.5s-chat"):
        import requests
        api_key = os.getenv("MINIMAX_API_KEY")
        group_id = os.getenv("MINIMAX_GROUP_ID")
        if not api_key:
            raise ValueError("请在.env中设置 MINIMAX_API_KEY")
        if not group_id:
            raise ValueError("请在.env中设置 MINIMAX_GROUP_ID")
        self.api_key = api_key
        self.group_id = group_id
        self.model = model
        self.base_url = "https://api.minimax.chat/v1"
    
    def chat(self, system_prompt: str, user_message: str) -> str:
        import requests
        
        url = f"{self.base_url}/text/chatcompletion_v2"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API请求失败: {response.status_code} - {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]


# ============== 工厂函数 ==============
def get_llm_client(provider: str = None) -> LLMClient:
    """
    获取LLM客户端
    
    参数:
        provider: API提供商，可选值:
            - "demo" (演示模式，不需要API)
            - "openai" / "gpt"
            - "zhipu" / "glm"
            - "claude" / "anthropic"
            - "minimax" / "abab"
    
    也可以通过环境变量 LLM_PROVIDER 设置默认provider
    """
    # 如果没有指定，从环境变量读取
    if provider is None:
        provider = os.getenv("LLM_PROVIDER", "demo")
    
    provider = provider.lower()
    
    if provider == "demo":
        return DemoClient()
    
    elif provider in ["openai", "gpt"]:
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        return OpenAIClient(model=model)
    
    elif provider in ["zhipu", "glm"]:
        model = os.getenv("ZHIPU_MODEL", "glm-4")
        return ZhipuClient(model=model)
    
    elif provider in ["claude", "anthropic"]:
        model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
        return ClaudeClient(model=model)
    
    elif provider in ["minimax", "abab"]:
        model = os.getenv("MINIMAX_MODEL", "abab6.5s-chat")
        return MiniMaxClient(model=model)
    
    else:
        # 默认使用演示模式
        print(f"警告: 未知的Provider '{provider}'，使用演示模式")
        return DemoClient()


# ============== 向后兼容 ==============
_llm_client = None

def get_openai_client() -> LLMClient:
    """获取LLM客户端"""
    global _llm_client
    if _llm_client is None:
        _llm_client = get_llm_client()
    return _llm_client