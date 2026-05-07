# BID_demo

商业模式教学小组研究Agent系统

## 功能

- 小组初始化：输入课题和成员信息
- AI对话：与Agent多轮交互
- 分工规划：根据成员特点生成任务分配
- 会议引导：生成议程、会议主持、生成纪要
- 项目状态：自动维护项目进度

## 技术栈

- Streamlit（前端）
- OpenAI GPT-4o（LLM）

## 安装

```bash
pip install -r requirements.txt
```

## 配置

创建 `.env` 文件，添加：
```
OPENAI_API_KEY=你的API_KEY
```

## 运行

```bash
streamlit run app/main.py
```

## 部署

代码推送到GitHub后，通过 Streamlit Cloud 部署。