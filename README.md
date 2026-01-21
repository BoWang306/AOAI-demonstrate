# GPT 聊天测试

支持文本、图片和实时语音对话。

## 功能

### 💬 聊天测试（主页）
- 文本和图片输入
- 使用 Responses API
- 支持 Reasoning 参数
- 性能指标显示

### 🎤 Realtime Audio（语音页面）
- 实时语音对话
- WebRTC 技术
- 麦克风输入
- 实时转录

## 配置说明

配置保存在 `config.json` 文件中，包含两个独立的模型配置：

```json
{
  "chat": {
    "api_key": "聊天模型的 API Key",
    "endpoint": "https://your-resource.openai.azure.com/openai/deployments/your-model",
    "model": "gpt-4o"
  },
  "realtime": {
    "api_key": "Realtime 模型的 API Key",
    "endpoint": "https://your-resource.openai.azure.com",
    "deployment": "gpt-4o-realtime-preview"
  }
}
```

### 为什么需要分开配置？

- **聊天模型**: 使用 Responses API，支持文本和图片
- **Realtime 模型**: 使用 WebRTC，仅支持实时语音

两个模型的 API 接口不同，所以需要分别配置。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py
```

## 配置步骤

### 1. 配置聊天模型
1. 打开主页（💬 聊天测试）
2. 在侧边栏输入：
   - API Key
   - Endpoint (Base URL)
   - 模型名称
3. 点击 "💾 保存聊天配置"

### 2. 配置 Realtime 模型
1. 打开 🎤 Realtime Audio 页面
2. 在侧边栏输入：
   - API Key
   - Endpoint
   - Deployment Name
3. 点击 "💾 保存 Realtime 配置"

## 使用说明

### 聊天模式
1. 输入文本消息
2. （可选）上传图片
3. 选择 Reasoning 级别
4. 发送消息

### 语音模式
1. 点击 "🎤 开始对话"
2. 允许麦克风权限
3. 开始说话
4. 查看实时转录

## 注意事项

- 配置文件 `config.json` 包含敏感信息，已加入 `.gitignore`
- 两个模型可以使用不同的 API Key 和 Endpoint
- Realtime 模型需要浏览器支持 WebRTC

就这么简单！
