# 📋 模型配置管理指南

## 概述

本文档详细说明如何使用模型配置管理功能来管理多个 Azure OpenAI 模型的配置。

## 功能特性

### 1. 统一配置管理
- 在一个页面中管理所有模型配置
- 支持添加、编辑、删除、复制配置
- 配置持久化存储在 `model_configs.json` 文件中

### 2. 推理参数支持
- 支持 GPT-5 系列和 o 系列模型的推理参数
- 推理级别: none, minimal, low, medium, high
- 自动检测模型是否支持推理功能

### 3. 配置导入导出
- 导出配置文件用于备份
- 从备份文件导入配置
- JSON 格式,易于编辑和分享

### 4. 连接测试
- 测试配置是否可用
- 验证 API Key 和 Endpoint
- 实时反馈连接状态

## 使用方法

### 添加新配置

1. 打开 **模型配置管理** 页面
2. 点击左侧的 **➕ 添加新配置** 按钮
3. 填写必填字段:
   - **模型名称**: Azure OpenAI 部署的模型名称 (例如: gpt-5.2)
   - **Endpoint URL**: Azure OpenAI 资源的 endpoint (例如: https://your-resource.openai.azure.com)
   - **API Key**: Azure OpenAI 资源的 API key
4. 填写可选字段:
   - **API Version**: API 版本 (默认: 2024-02-15-preview)
   - **描述**: 配置的用途描述
5. 配置推理参数 (仅 GPT-5 系列和 o 系列):
   - 启用/禁用推理模式
   - 选择推理级别
6. 点击 **🧪 测试连接** 验证配置
7. 点击 **💾 保存配置** 保存

### 管理现有配置

#### 查看配置
- 配置以卡片形式展示
- 展开 **📖 查看配置详情** 查看完整信息

#### 编辑配置
1. 点击配置卡片的 **✏️ 编辑** 按钮
2. 修改配置信息
3. 点击 **💾 保存配置**

#### 复制配置
1. 点击配置卡片的 **📋 复制** 按钮
2. 系统自动创建一个副本 (名称后缀 -copy)
3. 可以修改副本的配置

#### 删除配置
1. 点击配置卡片的 **🗑️ 删除** 按钮
2. 再次点击确认删除

#### 测试配置
1. 点击配置卡片的 **🧪 测试** 按钮
2. 系统发送测试请求
3. 显示连接成功或失败信息

### 搜索和过滤

#### 搜索配置
在搜索框中输入模型名称或描述进行搜索

#### 过滤配置
使用 **过滤推理模式** 下拉菜单:
- **全部**: 显示所有配置
- **已启用**: 只显示启用推理的配置
- **未启用**: 只显示未启用推理的配置

### 导入导出配置

#### 导出配置
1. 点击左侧的 **📥 导出配置文件** 按钮
2. 下载 JSON 文件 (文件名包含时间戳)
3. 保存到安全位置

#### 导入配置
1. 点击左侧的 **📤 导入配置文件** 按钮
2. 选择 JSON 配置文件
3. 点击 **确认导入**
4. 系统将替换现有配置

## 在主应用中使用配置

### 配置模式选择

在主应用的侧边栏中:
1. 选择 **📁 从配置文件加载** 模式
2. 从下拉菜单中选择已保存的配置
3. 系统自动加载配置信息:
   - API Key
   - Endpoint
   - API Version
   - 推理参数

### 手动输入模式

如果选择 **📝 手动输入** 模式:
- 手动输入 API Key、Endpoint、API Version
- 从预定义模型列表中选择模型
- 不支持推理参数配置

## 配置文件格式

### 文件位置
`model_configs.json`

### 文件结构
```json
[
  {
    "id": 1,
    "model_name": "gpt-5.2",
    "endpoint": "https://your-resource.openai.azure.com",
    "api_key": "your-api-key",
    "api_version": "2024-02-15-preview",
    "reasoning_enabled": true,
    "reasoning_effort": "low",
    "description": "GPT-5.2 with low reasoning",
    "created_at": "2026-01-20T00:00:00",
    "updated_at": "2026-01-20T00:00:00"
  }
]
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | ✅ | 配置的唯一标识符 |
| model_name | string | ✅ | 模型名称 |
| endpoint | string | ✅ | Azure OpenAI endpoint URL |
| api_key | string | ✅ | API key |
| api_version | string | ⭕ | API 版本 (默认: 2024-02-15-preview) |
| reasoning_enabled | boolean | ⭕ | 是否启用推理模式 (默认: false) |
| reasoning_effort | string | ⭕ | 推理级别 (none/minimal/low/medium/high) |
| description | string | ⭕ | 配置描述 |
| created_at | string | ⭕ | 创建时间 (ISO 8601) |
| updated_at | string | ⭕ | 更新时间 (ISO 8601) |

## 推理参数详解

### 支持的模型
- GPT-5 系列: gpt-5, gpt-5-mini, gpt-5-nano, gpt-5-chat, gpt-5-pro
- GPT-5.1 系列: gpt-5.1, gpt-5.1-chat
- GPT-5.2 系列: gpt-5.2, gpt-5.2-chat, gpt-5.2-codex
- o 系列: o1, o1-mini, o3-mini

### 推理级别说明

| 级别 | 说明 | 适用场景 |
|------|------|---------|
| none | 标准响应,不使用推理能力 | 简单问答、快速响应 |
| minimal | 最小推理 | 轻量任务、需要快速响应 |
| low | 低推理 | 一般任务、平衡速度和质量 |
| medium | 中等推理 | 复杂任务、需要深入分析 |
| high | 高推理 | 非常复杂的任务、最高质量要求 |

### 推理级别选择建议

#### none / minimal
- ✅ 简单对话
- ✅ 信息查询
- ✅ 快速响应场景
- ✅ 大批量测试

#### low
- ✅ 常规问答
- ✅ 内容生成
- ✅ 代码解释
- ✅ 数据分析

#### medium
- ✅ 复杂问题解决
- ✅ 代码生成
- ✅ 深度分析
- ✅ 技术文档编写

#### high
- ✅ 研究性问题
- ✅ 算法设计
- ✅ 系统架构设计
- ✅ 关键决策支持

## 示例配置

### 示例 1: GPT-5.2 标准配置

```json
{
  "id": 1,
  "model_name": "gpt-5.2",
  "endpoint": "https://your-resource.openai.azure.com",
  "api_key": "your-api-key",
  "api_version": "2024-02-15-preview",
  "reasoning_enabled": false,
  "reasoning_effort": "none",
  "description": "GPT-5.2 standard configuration"
}
```

### 示例 2: GPT-5.2 启用推理

```json
{
  "id": 2,
  "model_name": "gpt-5.2",
  "endpoint": "https://your-resource.openai.azure.com",
  "api_key": "your-api-key",
  "api_version": "2024-02-15-preview",
  "reasoning_enabled": true,
  "reasoning_effort": "low",
  "description": "GPT-5.2 with low reasoning"
}
```

### 示例 3: GPT-5 最小推理

```json
{
  "id": 3,
  "model_name": "gpt-5",
  "endpoint": "https://your-resource-2.openai.azure.com",
  "api_key": "your-api-key-2",
  "api_version": "2024-02-15-preview",
  "reasoning_enabled": true,
  "reasoning_effort": "minimal",
  "description": "GPT-5 with minimal reasoning for fast responses"
}
```

### 示例 4: 多个配置

您可以为同一个模型创建多个配置,使用不同的推理级别:

```json
[
  {
    "id": 1,
    "model_name": "gpt-5.2",
    "reasoning_enabled": false,
    "description": "Fast responses"
  },
  {
    "id": 2,
    "model_name": "gpt-5.2",
    "reasoning_enabled": true,
    "reasoning_effort": "low",
    "description": "Balanced"
  },
  {
    "id": 3,
    "model_name": "gpt-5.2",
    "reasoning_enabled": true,
    "reasoning_effort": "high",
    "description": "Best quality"
  }
]
```

## 安全最佳实践

### 1. API Key 管理

⚠️ **重要**: API Key 以明文形式存储在配置文件中

**建议**:
- ❌ 不要将配置文件提交到公共代码仓库
- ✅ 添加 `model_configs.json` 到 `.gitignore`
- ✅ 适当设置文件访问权限 (chmod 600)
- ✅ 定期更换 API Key
- ✅ 在生产环境中使用 Azure Key Vault

### 2. 环境变量

可以使用环境变量替代配置文件中的敏感信息:

```bash
# .env 文件
AZURE_ENDPOINT_5x=https://your-resource.openai.azure.com
API_KEY_5x=your-api-key-here
```

然后在配置文件中使用:
```json
{
  "endpoint": "${AZURE_ENDPOINT_5x}",
  "api_key": "${API_KEY_5x}"
}
```

### 3. 访问控制

- 限制配置文件的读取权限
- 仅授权用户可以访问配置管理页面
- 定期审计配置更改

### 4. 备份和恢复

- 定期导出配置文件备份
- 将备份存储在安全位置
- 测试恢复流程

## 故障排查

### 配置加载失败

**问题**: 配置文件无法加载

**解决方案**:
1. 检查文件是否存在: `model_configs.json`
2. 检查 JSON 格式是否正确
3. 检查文件权限
4. 查看控制台错误信息

### 连接测试失败

**问题**: 测试连接时失败

**解决方案**:
1. 验证 API Key 是否正确
2. 验证 Endpoint URL 是否正确
3. 检查网络连接
4. 确认模型已部署在 Azure OpenAI 资源中
5. 检查 API 配额

### 推理参数不生效

**问题**: 启用推理参数后没有效果

**解决方案**:
1. 确认模型支持推理参数
2. 检查 `reasoning_enabled` 是否为 `true`
3. 检查 `reasoning_effort` 值是否有效
4. 在主应用中选择 "从配置文件加载" 模式

### 模型选择错误

**问题**: 选择的模型无法使用

**解决方案**:
1. 确认模型名称与 Azure 部署名称一致
2. 检查模型是否需要注册
3. 验证 API 版本是否支持该模型
4. 参考 MODEL_COMPATIBILITY.md 文档

## 高级用法

### 批量创建配置

可以手动编辑 `model_configs.json` 文件批量添加配置:

```bash
# 1. 导出现有配置作为模板
# 2. 编辑 JSON 文件添加新配置
# 3. 在配置管理页面导入
```

### 配置版本控制

使用 Git 管理配置文件 (注意安全):

```bash
# 1. 创建一个模板配置文件
cp model_configs.json model_configs.template.json

# 2. 替换敏感信息为占位符
# 3. 提交模板到 Git
git add model_configs.template.json
git commit -m "Add config template"

# 4. 添加实际配置到 .gitignore
echo "model_configs.json" >> .gitignore
```

### 多环境配置

为不同环境创建不同的配置:

```bash
model_configs.dev.json    # 开发环境
model_configs.test.json   # 测试环境
model_configs.prod.json   # 生产环境
```

## 常见问题 (FAQ)

### Q1: 配置文件存储在哪里?
**A**: 配置文件 `model_configs.json` 存储在应用根目录。

### Q2: 可以同时使用多个配置吗?
**A**: 一次只能激活一个配置,但可以创建多个配置并快速切换。

### Q3: 推理参数会影响性能吗?
**A**: 是的,推理级别越高,响应时间可能越长,但质量可能更好。

### Q4: 如何迁移配置到另一个系统?
**A**: 使用导出功能下载配置文件,然后在新系统上导入。

### Q5: 配置会自动同步吗?
**A**: 不会,配置存储在本地文件中,需要手动导出/导入。

### Q6: 可以使用环境变量吗?
**A**: 当前版本不支持,但可以手动替换配置文件中的值。

### Q7: 删除配置可以恢复吗?
**A**: 不能自动恢复,建议在删除前导出备份。

### Q8: 配置文件可以加密吗?
**A**: 当前版本不支持加密,建议使用文件系统权限和 Azure Key Vault。

## 更新日志

### Version 1.2.0 (2026-01-20)
- ✨ 添加模型配置管理页面
- ✨ 支持推理参数配置
- ✨ 添加配置导入导出功能
- ✨ 添加连接测试功能
- ✨ 主应用支持从配置文件加载
- 📖 添加完整配置管理文档

## 相关文档

- [README.md](README.md) - 项目概述
- [GUIDE.md](GUIDE.md) - 详细使用指南
- [MODEL_COMPATIBILITY.md](MODEL_COMPATIBILITY.md) - 模型兼容性说明
- [DOCKER.md](DOCKER.md) - Docker 部署指南

## 技术支持

如有问题或建议,请通过以下方式联系:
- GitHub Issues: https://github.com/BoWang306/AOAI-demonstrate/issues
- 文档: https://github.com/BoWang306/AOAI-demonstrate

---

**更新时间**: 2026-01-20  
**版本**: 1.2.0
