"""
LLM统一客户端 - 支持多种API
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
            - "openai" / "gpt" / None (默认)
            - "zhipu" / "glm"
            - "claude" / "anthropic"
    
    也可以通过环境变量 LLM_PROVIDER 设置默认provider
    """
    # 如果没有指定，从环境变量读取
    if provider is None:
        provider = os.getenv("LLM_PROVIDER", "openai")
    
    provider = provider.lower()
    
    if provider in ["openai", "gpt"]:
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
        raise ValueError(f"不支持的Provider: {provider}")


# ============== 向后兼容 ==============
# 为了保持向后兼容，提供一个简单的封装
class OpenAIClientLegacy:
    """兼容旧代码的OpenAI客户端"""
    
    def __init__(self):
        self._client = get_llm_client("openai")
    
    def chat(self, system_prompt: str, user_message: str) -> str:
        return self._client.chat(system_prompt, user_message)


# 全局客户端实例
_llm_client = None

def get_openai_client() -> LLMClient:
    """获取LLM客户端（兼容旧代码）"""
    global _llm_client
    if _llm_client is None:
        provider = os.getenv("LLM_PROVIDER", "openai")
        _llm_client = get_llm_client(provider)
    return _llm_client