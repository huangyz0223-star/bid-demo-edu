# GroupMind

> 小组研究智能助手 - 商业模式教学AI Agent系统

## 产品定位

**GroupMind = Group（小组）+ Mind（智能）**

帮助大学小组完成商业模式研究课题的AI助手。

## 核心功能

- 📝 **项目初始化**：输入课题和成员信息，AI自动生成研究计划
- 💬 **智能对话**：与AI助手多轮交互，获得专业建议
- 📋 **分工规划**：根据成员特点自动生成任务分配
- 📅 **会议引导**：自动生成议程、主持会议、生成纪要
- 📊 **进度追踪**：自动维护项目状态和成果

## 技术栈

- Streamlit（前端）
- LLM（支持OpenAI/智谱GLM/Claude/MiniMax）

## 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 配置

创建 `.env` 文件：

```env
# 使用演示模式（无需API Key）
LLM_PROVIDER=demo

# 或使用真实API
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key
```

### 运行

```bash
streamlit run app/main.py
```

## 部署

代码推送到GitHub后，通过 [Streamlit Cloud](https://share.streamlit.io) 部署。

## License

MIT