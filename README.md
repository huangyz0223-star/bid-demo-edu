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
- LLM（支持OpenAI/智谱GLM/Claude/MiniMax）

## 安装

```bash
pip install -r requirements.txt
```

## 配置

创建 `.env` 文件，添加以下配置：

### 使用OpenAI
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key
OPENAI_MODEL=gpt-4o
```

### 使用智谱GLM
```env
LLM_PROVIDER=zhipu
ZHIPU_API_KEY=your-zhipu-api-key
ZHIPU_MODEL=glm-4
```

### 使用Claude
```env
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=your-anthropic-api-key
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

### 使用MiniMax
```env
LLM_PROVIDER=minimax
MINIMAX_API_KEY=your-minimax-api-key
MINIMAX_GROUP_ID=your-group-id
MINIMAX_MODEL=abab6.5s-chat
```

## 运行

```bash
streamlit run app/main.py
```

## 部署

代码推送到GitHub后：

1. 访问 [Streamlit Cloud](https://share.streamlit.io)
2. 点击 "New app"
3. 选择 `huangyz0223-star/bid-demo-edu` 仓库
4. Branch: `main`
5. Main file: `app/main.py`
6. 在 Advanced settings 中添加环境变量（API Key等）
7. 点击 "Deploy!"

部署成功后，你会获得一个 `xxx.streamlit.app` 的链接，可以分享给任何人试用。