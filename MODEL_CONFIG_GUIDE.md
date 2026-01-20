# 模型配置管理器使用指南

## 📖 概述

模型配置管理器是一个独立的页面，用于统一管理多个 Azure OpenAI 模型的配置。支持：

- 🔧 配置多个模型实例
- 🔑 管理不同的 endpoint 和 API key
- ⚡ 设置 reasoning_effort（推理强度）
- ✅ 启用/禁用特定配置
- 🧪 测试连接
- 💾 导入/导出配置

## 🚀 快速开始

### 启动配置管理器

```bash
# 方式 1: 直接运行
streamlit run model_config_manager.py

# 方式 2: 从主应用跳转
# 在主应用侧边栏点击 "🔧 打开配置管理器"
```

访问: http://localhost:8502

## ⚙️ 配置项说明

### 基本配置

| 字段 | 说明 | 示例 |
|------|------|------|
| **模型名称** | Azure OpenAI 部署的模型名称 | `gpt-5.2`, `gpt-5-nano` |
| **Endpoint URL** | Azure OpenAI 资源的端点 | `https://xxx.openai.azure.com/` |
| **API Key** | Azure OpenAI 的访问密钥 | `sk-...` |
| **API Version** | API 版本 | `2024-02-15-preview` |
| **描述** | 配置的描述/用途 | `生产环境`, `测试环境` |

### Reasoning Effort (推理强度)

控制模型的推理深度和质量：

| 选项 | 说明 | 适用场景 | 速度 | 质量 |
|------|------|----------|------|------|
| **none** | 无推理 | 快速响应场景 | ⚡⚡⚡⚡⚡ | ⭐⭐ |
| **minimal** | 最小推理 | 简单任务 | ⚡⚡⚡⚡ | ⭐⭐⭐ |
| **low** | 低强度推理 | 一般任务 | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| **medium** | 中等推理 | 复杂任务 | ⚡⚡ | ⭐⭐⭐⭐⭐ |
| **high** | 高强度推理 | 困难任务 | ⚡ | ⭐⭐⭐⭐⭐⭐ |
| **xhigh** | 超高推理 | 极端困难任务 | ⚡ | ⭐⭐⭐⭐⭐⭐⭐ |

**注意**:
- 推理强度越高，响应速度越慢，但质量越好
- 并非所有模型都支持所有级别
- `xhigh` 仅部分高级模型支持

## 📝 配置示例

### 示例 1: 同一模型不同推理强度

适用于需要在速度和质量之间权衡的场景：

```json
{
  "configs": [
    {
      "model_name": "gpt-5.2",
      "endpoint": "https://myresource.openai.azure.com/",
      "api_key": "sk-xxx",
      "api_version": "2024-02-15-preview",
      "reasoning_effort": "none",
      "enabled": true,
      "description": "快速响应 - 用于简单任务"
    },
    {
      "model_name": "gpt-5.2",
      "endpoint": "https://myresource.openai.azure.com/",
      "api_key": "sk-xxx",
      "api_version": "2024-02-15-preview",
      "reasoning_effort": "low",
      "enabled": true,
      "description": "标准推理 - 用于一般任务"
    },
    {
      "model_name": "gpt-5.2",
      "endpoint": "https://myresource.openai.azure.com/",
      "api_key": "sk-xxx",
      "api_version": "2024-02-15-preview",
      "reasoning_effort": "high",
      "enabled": true,
      "description": "深度推理 - 用于复杂任务"
    }
  ]
}
```

### 示例 2: 多个模型多个环境

适用于同时管理多个部署环境：

```json
{
  "configs": [
    {
      "model_name": "gpt-5.2",
      "endpoint": "https://prod.openai.azure.com/",
      "api_key": "sk-prod-xxx",
      "api_version": "2024-02-15-preview",
      "reasoning_effort": "low",
      "enabled": true,
      "description": "生产环境 - GPT-5.2"
    },
    {
      "model_name": "gpt-5-nano",
      "endpoint": "https://test.openai.azure.com/",
      "api_key": "sk-test-xxx",
      "api_version": "2024-02-15-preview",
      "reasoning_effort": "minimal",
      "enabled": true,
      "description": "测试环境 - GPT-5-nano"
    },
    {
      "model_name": "gpt-4.1-nano",
      "endpoint": "https://dev.openai.azure.com/",
      "api_key": "sk-dev-xxx",
      "api_version": "2024-02-15-preview",
      "reasoning_effort": "none",
      "enabled": false,
      "description": "开发环境 - GPT-4.1-nano (已禁用)"
    }
  ]
}
```

### 示例 3: 不同区域的部署

适用于全球部署的应用：

```json
{
  "configs": [
    {
      "model_name": "gpt-5",
      "endpoint": "https://eastus.openai.azure.com/",
      "api_key": "sk-eastus-xxx",
      "reasoning_effort": "low",
      "enabled": true,
      "description": "美国东部"
    },
    {
      "model_name": "gpt-5",
      "endpoint": "https://westeurope.openai.azure.com/",
      "api_key": "sk-westeu-xxx",
      "reasoning_effort": "low",
      "enabled": true,
      "description": "西欧"
    },
    {
      "model_name": "gpt-5",
      "endpoint": "https://japaneast.openai.azure.com/",
      "api_key": "sk-japan-xxx",
      "reasoning_effort": "low",
      "enabled": true,
      "description": "日本东部"
    }
  ]
}
```

## 🎯 使用场景

### 场景 1: A/B 测试

配置同一模型的不同推理强度，测试哪个最适合你的用例：

1. 添加 3 个配置，使用不同的 `reasoning_effort`
2. 在测试中对比响应速度和质量
3. 禁用不需要的配置
4. 在生产中使用最优配置

### 场景 2: 多环境管理

管理开发、测试、生产环境的配置：

1. 为每个环境创建独立配置
2. 使用描述字段标记环境
3. 开发时启用开发环境配置
4. 生产部署时切换到生产配置

### 场景 3: 成本优化

根据任务复杂度选择合适的配置：

- **简单任务**: 使用 `none` 或 `minimal`，节省成本
- **中等任务**: 使用 `low`，平衡成本和质量
- **复杂任务**: 使用 `high`，确保质量

### 场景 4: 负载均衡

配置多个相同模型，分散到不同的 endpoint：

1. 创建多个相同模型的配置
2. 使用不同的 endpoint（不同区域）
3. 应用程序轮询使用这些配置
4. 实现简单的负载均衡

## 🔧 高级功能

### 1. 测试连接

点击 "🧪 测试连接" 按钮：
- 验证 endpoint 和 API key 是否正确
- 测试模型是否已部署
- 查看实际响应和 token 使用量

### 2. 复制配置

点击 "📋 复制配置" 按钮：
- 快速创建相似配置
- 只需修改少量参数
- 节省配置时间

### 3. 导出/导入

**导出**:
1. 点击侧边栏的 "📤 导出配置"
2. 下载 JSON 文件
3. 备份或分享给团队

**导入**:
1. 编辑 `model_configs.json` 文件
2. 放置在项目根目录
3. 重新加载配置管理器

### 4. 启用/禁用

- 禁用的配置不会在主应用中显示
- 用于暂时停用某些配置
- 保留配置信息，随时可重新启用

## 📋 配置文件格式

配置保存在 `model_configs.json` 文件中：

```json
{
  "configs": [
    {
      "model_name": "模型名称",
      "endpoint": "Endpoint URL",
      "api_key": "API Key",
      "api_version": "API 版本",
      "reasoning_effort": "推理强度",
      "enabled": true/false,
      "description": "描述"
    }
  ]
}
```

## 🔒 安全最佳实践

### 1. 保护配置文件

```bash
# 不要提交配置文件到 Git
echo "model_configs.json" >> .gitignore

# 设置文件权限
chmod 600 model_configs.json
```

### 2. 使用环境变量（可选）

创建配置模板，使用环境变量：

```json
{
  "configs": [
    {
      "model_name": "gpt-5.2",
      "endpoint": "${AZURE_ENDPOINT_5x}",
      "api_key": "${API_KEY_5x}",
      ...
    }
  ]
}
```

### 3. 分离敏感信息

- 开发环境使用测试密钥
- 生产环境使用生产密钥
- 定期轮换 API 密钥

## 🐛 故障排查

### 问题 1: 配置未加载

**解决方案**:
```bash
# 检查文件是否存在
ls -la model_configs.json

# 验证 JSON 格式
cat model_configs.json | jq

# 重新启动应用
streamlit run model_config_manager.py
```

### 问题 2: 测试连接失败

**常见原因**:
1. Endpoint URL 格式错误（确保以 `/` 结尾）
2. API Key 无效或过期
3. 模型未在 Azure OpenAI Studio 中部署
4. 网络连接问题

**检查步骤**:
```bash
# 测试网络连接
curl -I https://your-endpoint.openai.azure.com/

# 验证 API Key
# 在 Azure Portal 中重新获取密钥
```

### 问题 3: 推理强度不生效

某些模型不支持所有推理强度级别：

- 检查模型文档确认支持的级别
- 尝试使用较低的推理强度
- 查看错误消息获取详细信息

## 📊 最佳实践

### 1. 命名规范

使用清晰的描述：
- ✅ `生产环境 - GPT-5.2 - 高质量`
- ✅ `测试 - 快速响应 - GPT-5-nano`
- ❌ `配置1`, `test`

### 2. 组织配置

按用途分组：
```
configs:
  1. 生产环境配置
  2. 测试环境配置
  3. 开发环境配置
  4. 特殊用途配置
```

### 3. 定期审查

- 每月检查并清理不用的配置
- 更新过期的 API 密钥
- 测试所有启用的配置

### 4. 文档化

在描述字段记录：
- 使用场景
- 负责人
- 创建日期
- 特殊注意事项

## 🔗 相关文档

- [主应用文档](README.md)
- [模型兼容性指南](MODEL_COMPATIBILITY.md)
- [Docker 部署指南](DOCKER.md)
- [详细使用指南](GUIDE.md)

## 💡 提示

- 配置管理器是一个独立页面，可单独运行
- 配置文件在主应用和配置管理器之间共享
- 修改配置后无需重启主应用

---

**版本**: 1.0  
**最后更新**: 2026-01-16
