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

点击 **💾 保存配置** 按钮保存配置到本地，下次打开自动加载。

## 功能

- 💬 多轮对话
- 🔄 流式输出
- ⚙️ 可调参数（Temperature、Max Completion Tokens）
- 🗑️ 清空对话历史
- 💾 配置保存（保存到本地 `config.json`）

## 更新日志

### v1.1
- ✅ 修复：使用 `max_completion_tokens` 替代 `max_tokens`（支持新版本 API）
- ✅ 新增：配置保存功能，自动加载上次配置

就这么简单！
