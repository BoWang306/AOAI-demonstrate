# Azure OpenAI 模型测试门户 - 快速参考

## 🚀 快速启动

```bash
# 方法 1: 直接启动
streamlit run app.py

# 方法 2: 使用脚本
./start.sh

# 方法 3: 配置助手
streamlit run config_helper.py
```

## 📁 项目结构

```
webapp/
├── app.py                      # 主应用程序
├── config_helper.py            # API 配置助手
├── start.sh                    # 启动脚本
├── requirements.txt            # Python 依赖
├── test_cases_example.json     # 批量测试示例
├── .env.example                # 环境变量模板
├── .gitignore                  # Git 忽略配置
├── README.md                   # 项目说明
└── GUIDE.md                    # 详细使用指南
```

## 🎯 支持的模型

| 系列 | 模型 | 用途 |
|------|------|------|
| **GPT-4.1** | gpt-4.1-nano | 快速响应 |
| **GPT-5** | gpt-5, gpt-5-nano, gpt-5-pro | 通用任务 |
| **GPT-5.1** | gpt-5.1-chat | 对话优化 |
| **GPT-5.2** | gpt-5.2, gpt-5.2-chat, gpt-5.2-chat-2, gpt-5.2-codex | 多功能 |
| **GPT-Realtime** | gpt-realtime | 实时对话 |
| **Grok** | grok-4-fast-non-reasoning | 快速推理 |

## ⚙️ 关键参数

| 参数 | 范围 | 默认值 | 说明 |
|------|------|--------|------|
| **Temperature** | 0.0 - 2.0 | 0.7 | 控制随机性 |
| **Max Tokens** | 100 - 4000 | 1000 | 最大输出长度 |
| **Top P** | 0.0 - 1.0 | 0.95 | 核采样 |
| **Stream** | True/False | False | 流式输出 |

## 🎨 使用场景

### 场景 1: 代码生成
```
Model: gpt-5.2-codex
Temperature: 0.2
Max Tokens: 2000
System: "你是一个专业的程序员"
```

### 场景 2: 创意写作
```
Model: gpt-5-pro
Temperature: 0.9
Max Tokens: 1500
System: "你是一个创意作家"
```

### 场景 3: 数据分析
```
Model: gpt-5
Temperature: 0.3
Max Tokens: 1000
System: "你是一个数据分析师"
```

### 场景 4: 快速问答
```
Model: gpt-5-nano
Temperature: 0.5
Max Tokens: 500
Stream: True
```

## 🔧 配置模板

### .env 文件
```env
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 批量测试 JSON
```json
[
  {
    "name": "测试用例名称",
    "prompt": "你的提示词内容"
  }
]
```

## 📊 性能指标

| 指标 | 说明 |
|------|------|
| **延迟 (Latency)** | API 响应时间 |
| **输入 Tokens** | Prompt token 数量 |
| **输出 Tokens** | 生成 token 数量 |
| **总计 Tokens** | 总 token 使用量 |

## ⚡ 快捷键

| 操作 | 快捷键/方法 |
|------|------------|
| 发送消息 | Enter |
| 清空历史 | 侧边栏按钮 |
| 停止生成 | Ctrl+C |
| 重启应用 | Ctrl+R |

## 🐛 故障排查

| 问题 | 解决方案 |
|------|----------|
| 连接失败 | 检查 API Key 和 Endpoint |
| 模型不存在 | 验证模型部署名称 |
| 配额超限 | 检查 Azure 订阅配额 |
| 响应慢 | 使用 nano 模型或流式输出 |

## 📞 获取帮助

1. 查看 `GUIDE.md` 详细文档
2. 运行配置助手: `streamlit run config_helper.py`
3. 查看示例: `test_cases_example.json`
4. 访问 Azure OpenAI 文档

## 🔗 相关链接

- **Azure Portal**: https://portal.azure.com
- **Azure OpenAI Studio**: https://oai.azure.com
- **Streamlit 文档**: https://docs.streamlit.io
- **OpenAI API 文档**: https://platform.openai.com/docs

---

**快速参考卡片 v1.0** | 最后更新: 2026-01-16
