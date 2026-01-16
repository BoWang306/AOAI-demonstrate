# Azure OpenAI 模型测试门户

一个功能完整的 Streamlit Web 应用，用于测试和展示 Azure OpenAI 的各种模型和 API。

## 🌟 功能特点

### 1. 💬 聊天测试模式
- 多轮对话支持
- 保留对话历史
- 实时交互测试
- 流式/非流式输出切换

### 2. 📝 单次 API 调用
- 快速测试单个请求
- 自定义 System Prompt 和 User Prompt
- 查看详细响应 JSON
- 实时性能指标展示（延迟、Token 使用量）

### 3. 📊 批量测试工具
- 支持多个测试用例同时运行
- 手动输入或 JSON 文件上传
- 测试结果对比分析
- 汇总统计和结果导出

### 4. 📖 模型信息展示
- 完整的模型列表
- 分类展示（GPT-4.1、GPT-5 系列等）
- 使用指南和参数说明

## 🎯 支持的模型

当前支持以下模型系列：

### GPT-4.1 系列
- gpt-4.1-nano

### GPT-5 系列
- gpt-5
- gpt-5-nano
- gpt-5-pro

### GPT-5.1 系列
- gpt-5.1-chat

### GPT-5.2 系列
- gpt-5.2
- gpt-5.2-chat
- gpt-5.2-chat-2
- gpt-5.2-codex

### GPT-Realtime 系列
- gpt-realtime

### Grok 系列
- grok-4-fast-non-reasoning

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
streamlit run app.py
```

### 3. 配置 API

在侧边栏输入：
- **API Key**: 你的 Azure OpenAI API 密钥
- **API Base URL**: Azure OpenAI 端点 URL（例如：`https://your-resource.openai.azure.com/`）
- **API Version**: API 版本（默认：`2024-02-15-preview`）

点击"保存配置"按钮保存设置。

## 📋 使用流程

### 聊天测试
1. 在侧边栏选择模型
2. 调整参数（Temperature、Max Tokens 等）
3. 在聊天框输入消息
4. 查看 AI 回复和性能指标

### 单次调用测试
1. 选择"单次调用"标签页
2. 输入 System Prompt（可选）和 User Prompt
3. 点击"发送请求"
4. 查看响应内容、性能指标和完整 JSON

### 批量测试
1. 选择"批量测试"标签页
2. 选择输入模式（手动输入或上传 JSON）
3. 配置测试用例
4. 点击"开始批量测试"
5. 查看结果并导出

#### 批量测试 JSON 格式示例

```json
[
  {
    "name": "测试用例1",
    "prompt": "解释什么是机器学习"
  },
  {
    "name": "测试用例2",
    "prompt": "写一首关于春天的诗"
  },
  {
    "name": "测试用例3",
    "prompt": "用 Python 实现快速排序"
  }
]
```

## ⚙️ 参数说明

| 参数 | 说明 | 范围 | 默认值 |
|------|------|------|--------|
| **Temperature** | 控制输出的随机性和创造性。值越高，输出越随机；值越低，输出越确定 | 0.0 - 2.0 | 0.7 |
| **Max Tokens** | 生成的最大 token 数量 | 100 - 4000 | 1000 |
| **Top P** | 核采样参数，控制考虑的词汇范围 | 0.0 - 1.0 | 0.95 |
| **流式输出** | 启用后实时显示生成的文本 | True/False | False |

## 📊 性能指标

应用会显示以下性能指标：

- **延迟 (Latency)**: API 调用的响应时间（秒）
- **输入 Tokens**: 发送给模型的 token 数量
- **输出 Tokens**: 模型生成的 token 数量
- **总计 Tokens**: 输入和输出 token 的总和

## 🔐 安全注意事项

- API Key 仅保存在当前浏览器会话中
- 不会上传到任何外部服务器
- 建议使用环境变量管理敏感信息
- 可以通过 `.env` 文件配置默认值

### 使用环境变量（可选）

创建 `.env` 文件：

```env
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

## 🎨 界面特点

- 🎯 直观的模型选择界面
- 📊 实时性能监控
- 💬 交互式聊天体验
- 📈 批量测试结果可视化
- 🔧 灵活的参数调整
- 📱 响应式设计

## 🛠️ 技术栈

- **Streamlit**: Web 应用框架
- **OpenAI Python SDK**: Azure OpenAI API 客户端
- **Python 3.8+**: 编程语言

## 📝 更新日志

### Version 1.0.0 (2026-01-16)
- ✨ 初始版本发布
- 💬 支持聊天测试模式
- 📝 支持单次 API 调用
- 📊 支持批量测试
- 📖 完整的模型信息展示
- 🎨 现代化 UI 设计

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

MIT License

## 📞 支持

如有问题或建议，请联系开发团队。

---

**祝使用愉快！🚀**
