"""
OpenAI API 封装
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("请在.env文件中设置OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
    
    def chat(self, system_prompt: str, user_message: str, model: str = "gpt-4o") -> str:
        """发送对话请求"""
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content


# 全局客户端实例
openai_client = None

def get_openai_client() -> OpenAIClient:
    global openai_client
    if openai_client is None:
        openai_client = OpenAIClient()
    return openai_client