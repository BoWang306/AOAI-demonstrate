# 更新日志

## Version 1.2.0 - 2026-01-20

### 🎉 主要新增功能

#### 模型配置管理系统
- **新增页面**: `模型配置管理` - 统一管理所有模型配置
- **配置功能**:
  - ✅ 添加新配置
  - ✅ 编辑现有配置
  - ✅ 删除配置（需二次确认）
  - ✅ 复制配置
  - ✅ 测试连接
- **批量操作**:
  - ✅ 导出配置文件（带时间戳）
  - ✅ 导入配置文件
- **搜索和过滤**:
  - ✅ 按模型名称或描述搜索
  - ✅ 按推理模式过滤

#### 推理参数支持
- **支持模型**: GPT-5 系列、GPT-5.1 系列、GPT-5.2 系列、o 系列
- **推理级别**:
  - `none`: 标准响应（不使用推理能力）
  - `minimal`: 最小推理
  - `low`: 低推理
  - `medium`: 中等推理
  - `high`: 高推理
- **自动检测**: 自动识别模型是否支持推理参数
- **UI 提示**: 不支持推理的模型会禁用相关选项

#### 主应用增强
- **配置模式切换**:
  - 📝 手动输入模式（原有方式）
  - 📁 配置文件加载模式（新增）
- **推理参数**: 从配置文件加载时自动应用推理参数
- **配置详情**: 实时显示选中配置的详细信息

### 📝 新增文档

- **CONFIG_GUIDE.md**: 完整的配置管理指南
  - 使用方法
  - 配置文件格式
  - 推理参数详解
  - 示例配置
  - 安全最佳实践
  - 故障排查
  - 常见问题

- **MODEL_CONFIG_GUIDE.md**: 快速上手指南
  - 基本操作
  - 配置示例
  - 使用建议

### 🔧 更新和改进

#### app.py
- ✅ 添加 `load_model_configs()` 函数
- ✅ 更新 `call_chat_completion()` 支持推理参数
- ✅ 重构侧边栏 UI
- ✅ 添加配置模式选择
- ✅ 所有 API 调用支持推理参数

#### README.md
- ✅ 更新功能列表
- ✅ 添加配置管理说明
- ✅ 更新 API 配置章节

### 📦 新增文件

```
pages/
  └── 1_🔧_模型配置管理.py  # 配置管理页面（18KB+）

model_configs.json            # 示例配置文件（包含 8 个配置）
CONFIG_GUIDE.md               # 配置管理完整指南
MODEL_CONFIG_GUIDE.md         # 配置管理快速指南
```

### 🔒 安全提示

⚠️ **重要**: 
- API Key 以明文形式存储在 `model_configs.json`
- 不要将配置文件提交到公共仓库
- 建议将 `model_configs.json` 添加到 `.gitignore`
- 生产环境建议使用 Azure Key Vault

### 📊 统计数据

- **新增代码**: 约 1,600+ 行
- **新增文件**: 4 个
- **更新文件**: 2 个
- **总提交**: 1 个大型功能提交

### 🎯 示例配置

项目包含 8 个示例配置：
1. GPT-5.2 (low reasoning)
2. GPT-5.2 (no reasoning)
3. GPT-5.1 (low reasoning)
4. GPT-5.1 (no reasoning)
5. GPT-5 (low reasoning)
6. GPT-5 (minimal reasoning)
7. GPT-5 Nano (low reasoning)
8. GPT-5 Nano (minimal reasoning)

### 🚀 使用方法

#### 快速开始

1. **访问配置管理页面**:
   ```
   导航到 模型配置管理 页面
   ```

2. **添加第一个配置**:
   - 点击 "➕ 添加新配置"
   - 填写模型信息
   - 配置推理参数（可选）
   - 保存并测试

3. **在主应用中使用**:
   - 返回主页
   - 选择 "📁 从配置文件加载"
   - 选择配置
   - 开始测试

#### 配置示例

```json
{
  "id": 1,
  "model_name": "gpt-5.2",
  "endpoint": "https://your-resource.openai.azure.com",
  "api_key": "your-api-key",
  "api_version": "2024-02-15-preview",
  "reasoning_enabled": true,
  "reasoning_effort": "low",
  "description": "GPT-5.2 with low reasoning"
}
```

### 🐛 已知问题

目前没有已知问题。

### 📖 相关文档

- [README.md](README.md) - 项目概述
- [CONFIG_GUIDE.md](CONFIG_GUIDE.md) - 配置管理完整指南
- [MODEL_CONFIG_GUIDE.md](MODEL_CONFIG_GUIDE.md) - 配置管理快速指南
- [MODEL_COMPATIBILITY.md](MODEL_COMPATIBILITY.md) - 模型兼容性
- [GUIDE.md](GUIDE.md) - 详细使用指南

### 🔗 链接

- **GitHub 仓库**: https://github.com/BoWang306/AOAI-demonstrate
- **应用访问**: https://8501-inzgvq26k1zwv3fwy7kx4-b237eb32.sandbox.novita.ai

---

## Version 1.1.0 - 2026-01-20 (早期更新)

### 修复和更新

- ✅ 更新模型列表（根据 Azure OpenAI 官方文档）
- ✅ 添加 API 兼容性检查
- ✅ 改进错误处理
- ✅ 添加 MODEL_COMPATIBILITY.md
- ✅ 简化 Dev Container 配置
- ✅ 移除 docker-compose 依赖（在 .devcontainer 中）
- ✅ 添加容器注册表支持
- ✅ 添加 build-and-push.sh 脚本

---

## Version 1.0.0 - 2026-01-16

### 初始版本

- ✅ 创建基础 Streamlit 应用
- ✅ 聊天测试功能
- ✅ 单次 API 调用
- ✅ 批量测试工具
- ✅ 模型信息展示
- ✅ Dev Container 支持
- ✅ Docker Compose 配置
- ✅ 完整文档（README、GUIDE、QUICKREF 等）

---

**最后更新**: 2026-01-20  
**当前版本**: 1.2.0
