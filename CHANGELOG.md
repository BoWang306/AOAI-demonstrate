# 更新日志 - v1.1.0

## 📅 更新时间: 2026-01-16

## 🎯 主要更新

### 1. ✅ 修复模型兼容性问题

**问题**: 之前版本中某些模型（如 `gpt-5-pro`）调用失败，提示 `OperationNotSupported` 错误。

**原因**: 这些模型仅支持 Responses API，不支持 Chat Completions API。

**解决方案**:
- 更新了完整的模型列表，标注每个模型支持的 API 类型
- 在界面上明确显示模型是否支持 Chat Completions API
- 添加了访问要求提示（需注册/无需注册）
- 改进了错误提示，提供详细的解决方案

### 2. 📊 更新模型列表

根据 Azure OpenAI 官方文档 (2025-01) 更新了所有模型系列：

#### 新增模型系列
- **GPT-4o 系列**: gpt-4o, gpt-4o-mini
- **GPT-4 Turbo**: gpt-4 (turbo-2024-04-09)
- **GPT-3.5 Turbo**: gpt-35-turbo
- **o 系列** (推理模型): o1, o1-mini, o3-mini

#### 更新现有模型
- **GPT-4.1**: 添加 gpt-4.1, gpt-4.1-mini
- **GPT-5**: 添加 gpt-5-mini, gpt-5-chat
- **GPT-5.1**: 添加 gpt-5.1
- **GPT-5.2**: 所有变体

#### 模型分类标注
每个模型现在都有：
- ✅ API 类型标识 (Chat Completions / Responses API)
- 📝 访问要求说明 (需注册/无需注册)
- 💡 模型描述 (标准版/迷你版/专业版等)

### 3. 🔧 改进错误处理

新增智能错误识别和友好提示：

#### OperationNotSupported 错误
```
❌ API 不支持错误
模型 `gpt-5-pro` 不支持 Chat Completions API

💡 解决方案:
1. 检查该模型是否需要使用 Responses API
2. 选择其他支持 Chat Completions API 的模型
3. 参考文档
```

#### DeploymentNotFound 错误
```
❌ 部署未找到
模型未在您的 Azure OpenAI 资源中部署

💡 解决方案:
1. 在 Azure OpenAI Studio 中部署该模型
2. 确保使用的是部署名称而不是模型名称
3. 检查部署是否在正确的区域
```

#### 其他错误类型
- 认证失败 (401 Unauthorized)
- 速率限制 (429 RateLimitReached)
- 请求参数错误 (invalid_request_error)
- 各类错误都有详细的解决方案

### 4. 📖 新增文档

#### MODEL_COMPATIBILITY.md
全面的模型兼容性指南，包含：
- 所有模型的 API 支持列表
- 访问要求和申请链接
- 常见错误和解决方案
- 最佳实践建议
- 代码示例

### 5. 🎨 界面改进

#### 模型选择界面
- 显示模型 API 支持状态 (✅ 绿色 / ⚠️ 黄色)
- 访问要求警告提示
- 模型详细信息展开查看

#### 模型信息页面
- 重新设计的模型列表展示
- API 类型彩色标签
- 访问要求和申请链接
- 常见错误说明
- 使用指南更新

## 📋 完整更新列表

### 代码更新
- ✅ 更新 `AVAILABLE_MODELS` 数据结构
- ✅ 改进 `call_chat_completion()` 错误处理
- ✅ 更新模型选择界面逻辑
- ✅ 重新设计 Tab 4 模型信息页面

### 文档更新
- ✅ 新增 `MODEL_COMPATIBILITY.md`
- ✅ 更新 `README.md`
- ✅ 更新 `CHANGELOG.md`

### 功能更新
- ✅ 模型 API 兼容性检查
- ✅ 智能错误识别和提示
- ✅ 访问要求提示
- ✅ 模型详情展开查看

## 🎯 使用建议

### 选择模型时
1. 查看模型是否标有 "✅ 支持 Chat Completions API"
2. 注意 "需注册" 的警告提示
3. 确保模型已在 Azure OpenAI Studio 中部署

### 遇到错误时
1. 阅读详细的错误提示
2. 按照提供的解决方案操作
3. 查看 MODEL_COMPATIBILITY.md 文档
4. 检查模型是否支持当前使用的 API

### 申请受限模型
访问相应链接申请访问：
- GPT-5 系列: https://aka.ms/oai/gpt5access
- GPT-Image 系列: https://aka.ms/oai/gptimage1access

## 🔗 相关资源

### 项目文档
- README.md - 项目主文档
- GUIDE.md - 详细使用指南
- MODEL_COMPATIBILITY.md - 模型兼容性指南
- DOCKER.md - Docker 部署指南

### 官方文档
- Azure OpenAI 文档: https://learn.microsoft.com/azure/ai-foundry/openai/
- 模型列表: https://learn.microsoft.com/azure/ai-foundry/foundry-models/
- Azure OpenAI Studio: https://oai.azure.com

## 📊 统计信息

- **新增模型系列**: 4 个
- **更新模型**: 20+ 个
- **新增文档**: 1 个
- **代码更新**: 4 处
- **错误类型覆盖**: 6 种

## 🚀 如何更新

### 如果已克隆项目
```bash
cd AOAI-demonstrate
git pull origin main
pip install -r requirements.txt
streamlit run app.py
```

### 如果使用 Docker
```bash
cd AOAI-demonstrate
git pull origin main
docker-compose -f .devcontainer/docker-compose.yml up -d --build
```

### 如果使用 Dev Container
1. 在 VS Code 中点击 "Reload Window"
2. 容器会自动重建并应用更新

## 🎉 体验更新

**在线访问**: https://8501-inzgvq26k1zwv3fwy7kx4-b237eb32.sandbox.novita.ai

现在你可以：
- ✅ 看到每个模型的 API 支持状态
- ✅ 获得更友好的错误提示
- ✅ 了解模型访问要求
- ✅ 查看完整的兼容性文档

## 💡 反馈和建议

如有问题或建议，请：
1. 查看 MODEL_COMPATIBILITY.md
2. 阅读错误提示信息
3. 访问官方文档
4. 在 GitHub 上提交 Issue

---

**版本**: v1.1.0  
**发布日期**: 2026-01-16  
**主要贡献**: 模型兼容性修复和错误处理改进
