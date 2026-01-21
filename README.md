# GPT 聊天测试

简单的 GPT 聊天界面，使用 Responses API，支持文本和图片输入。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py
```

## 配置

在侧边栏输入：
- **API Key**: Azure OpenAI API 密钥
- **Endpoint (Base URL)**: 完整的部署 URL
  - 格式：`https://your-resource.openai.azure.com/openai/deployments/your-model`
- **模型名称**: 模型名称（如 `gpt-4o`）

点击 **💾 保存配置** 按钮保存配置到本地，下次打开自动加载。

## 功能

- 💬 多轮对话
- 🖼️ 图片输入（支持 JPG、PNG）
- 🔄 流式输出（Responses API）
- 🧠 Reasoning 支持（GPT-5 系列、o 系列）
- 📊 性能指标（TTFT、总时长、Reasoning Tokens、Total Tokens）
- 🗑️ 清空对话历史
- 💾 配置保存（保存到本地 `config.json`）

## API 说明

本应用使用 OpenAI Responses API：
- 使用 `client.responses.create()` 而不是 `chat.completions.create()`
- 支持 `input_text` 和 `input_image` 输入格式
- 支持 `reasoning` 参数（effort: none/minimal/low/medium/high）

## 更新日志

### v2.0
- ✅ 改用 Responses API (`client.responses.create()`)
- ✅ 支持图片输入
- ✅ 支持 Reasoning 参数
- ✅ 显示详细性能指标（TTFT、Reasoning Tokens 等）

### v1.1
- ✅ 修复：使用 `max_completion_tokens` 替代 `max_tokens`
- ✅ 新增：配置保存功能

就这么简单！
