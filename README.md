# GPT 聊天测试

简单的 GPT 聊天界面，用于测试 Azure OpenAI 模型。

## 快速开始

```bash
# 安装依赖
pip install streamlit openai

# 运行应用
streamlit run app.py
```

## 配置

在侧边栏输入：
- **API Key**: Azure OpenAI API 密钥
- **Endpoint**: Azure OpenAI 端点（如 `https://your-resource.openai.azure.com/`）
- **模型名称**: 部署的模型名称（如 `gpt-4`）
- **API Version**: API 版本（默认 `2024-02-15-preview`）

## 功能

- 💬 多轮对话
- 🔄 流式输出
- ⚙️ 可调参数（Temperature、Max Tokens）
- 🗑️ 清空对话历史

就这么简单！
