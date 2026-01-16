# Azure OpenAI 模型 API 兼容性指南

## 📋 最后更新: 2025-01-16

根据 Azure OpenAI 官方文档，本文档列出了各模型系列支持的 API 类型和使用注意事项。

## 🎯 API 类型说明

### Chat Completions API
- 最常用的 API，支持对话式交互
- 支持流式和非流式输出
- 支持 function calling 和 structured outputs
- 大多数模型都支持此 API

### Responses API  
- 新一代 API，支持更多高级功能
- 某些模型仅支持此 API
- 支持 computer use 等特殊功能

## ✅ 模型兼容性列表

### GPT-4.1 系列
| 模型 | Chat Completions | Responses API | 注意事项 |
|------|-----------------|---------------|----------|
| gpt-4.1 | ✅ | ✅ | 标准版本 |
| gpt-4.1-mini | ✅ | ✅ | 迷你版本 |
| gpt-4.1-nano | ✅ | ✅ | 轻量快速版 |

**特性**:
- 文本和图像输入
- 最大上下文: 1,047,576 tokens
- 最大输出: 32,768 tokens

### GPT-5 系列
| 模型 | Chat Completions | Responses API | 访问要求 | 注意事项 |
|------|-----------------|---------------|----------|----------|
| gpt-5 | ✅ | ✅ | 需注册 | 标准版本 |
| gpt-5-mini | ✅ | ✅ | 无需注册 | 迷你版本 |
| gpt-5-nano | ✅ | ✅ | 无需注册 | 纳米版本 |
| gpt-5-chat | ✅ | ✅ | 无需注册 | 对话优化版 (Preview) |
| gpt-5-pro | ❌ | ✅ | 需注册 | **仅支持 Responses API** |

**访问申请**: https://aka.ms/oai/gpt5access

**特性**:
- 推理能力增强
- 文本和图像处理
- 最大上下文: 400,000 tokens
- 最大输出: 128,000 tokens

### GPT-5.1 系列
| 模型 | Chat Completions | Responses API | 访问要求 | 注意事项 |
|------|-----------------|---------------|----------|----------|
| gpt-5.1 | ✅ | ✅ | 需注册 | 标准版本 |
| gpt-5.1-chat | ✅ | ✅ | 无需注册 | 对话版 (Preview) |
| gpt-5.1-codex | ❌ | ✅ | 需注册 | **仅支持 Responses API** |
| gpt-5.1-codex-mini | ❌ | ✅ | 需注册 | **仅支持 Responses API** |

**访问申请**: https://aka.ms/oai/gpt5access

**重要提示**:
- `gpt-5.1` 的 `reasoning_effort` 默认为 `none`
- `gpt-5.1-chat` 增加了内置推理功能，不支持 temperature 参数

### GPT-5.2 系列
| 模型 | Chat Completions | Responses API | 访问要求 | 注意事项 |
|------|-----------------|---------------|----------|----------|
| gpt-5.2 | ✅ | ✅ | 需注册 | 标准版本 |
| gpt-5.2-chat | ✅ | ✅ | 无需注册 | 对话版 (Preview) |
| gpt-5.2-codex | ✅ | ✅ | 需注册 | 代码优化版 |

**访问申请**: https://aka.ms/oai/gpt5access

**特性**:
- 最新的 GPT 5 系列模型
- 推理和代码生成能力增强
- 最大上下文: 400,000 tokens

### GPT-4o 系列
| 模型 | Chat Completions | Responses API | 注意事项 |
|------|-----------------|---------------|----------|
| gpt-4o | ✅ | ✅ | GPT-4 Omni 标准版 |
| gpt-4o-mini | ✅ | ✅ | 快速经济版 |

**特性**:
- 多模态：文本和图像
- 最大上下文: 128,000 tokens
- JSON Mode 和 function calling
- 英语和多语言性能出色

### GPT-4 Turbo
| 模型 | Chat Completions | Responses API | 注意事项 |
|------|-----------------|---------------|----------|
| gpt-4 (turbo-2024-04-09) | ✅ | ✅ | GPT-4 Turbo with Vision |

**特性**:
- 替代所有之前的 GPT-4 preview 模型
- 最大上下文: 128,000 tokens

### GPT-3.5 系列
| 模型 | Chat Completions | Responses API | 注意事项 |
|------|-----------------|---------------|----------|
| gpt-35-turbo | ✅ | ✅ | 经典模型 |

**特性**:
- 经济实惠
- 适合大多数基础任务
- 最大上下文: 16,384 tokens (较新版本)

### o 系列 (推理模型)
| 模型 | Chat Completions | Responses API | 注意事项 |
|------|-----------------|---------------|----------|
| o1 | ✅ | ✅ | 推理模型 |
| o1-mini | ✅ | ✅ | 推理模型迷你版 |
| o3-mini | ✅ | ✅ | 新推理模型 |
| o4-mini | ✅ | ✅ | 最新推理模型 |
| codex-mini | ❌ | ✅ | **仅支持 Responses API** |

**特性**:
- 增强的推理能力
- 适合科学、编程、数学问题
- **不支持 temperature 参数**
- 需要更长的处理时间

### Grok 系列
| 模型 | Chat Completions | Responses API | 注意事项 |
|------|-----------------|---------------|----------|
| grok-4-fast-non-reasoning | ✅ | ✅ | 快速推理版本 |

**特性**:
- 快速响应
- 适合实时应用

## ⚠️ 常见错误和解决方案

### 错误 1: OperationNotSupported

```
Error code: 400 - {'error': {'code': 'OperationNotSupported', 
'message': 'The chatCompletion operation does not work with 
the specified model, gpt-5-pro.'}}
```

**原因**: 模型不支持 Chat Completions API

**解决方案**:
1. 检查模型兼容性表格
2. 使用 Responses API 代替
3. 或选择其他支持 Chat Completions API 的模型

**受影响的模型**:
- gpt-5-pro
- gpt-5.1-codex
- gpt-5.1-codex-mini
- codex-mini
- 以及其他标记为 "Responses API Only" 的模型

### 错误 2: DeploymentNotFound

```
Error code: 404 - {'error': {'code': 'DeploymentNotFound', 
'message': 'The API deployment for this resource does not exist.'}}
```

**原因**: 模型未部署或部署名称错误

**解决方案**:
1. 在 Azure OpenAI Studio 中部署模型
2. 确认使用**部署名称**而非模型名称
3. 检查部署状态是否为"成功"
4. 确认区域是否支持该模型

### 错误 3: 推理模型参数错误

```
Error code: 400 - {'error': {'code': 'invalid_request_error', 
'message': 'temperature is not supported for reasoning models'}}
```

**原因**: 推理模型（o 系列）不支持某些参数

**解决方案**:
1. 移除 `temperature` 参数
2. 移除 `top_p` 参数
3. 使用 `reasoning_effort` 代替（如果支持）

**受影响的模型**:
- o1, o1-mini
- o3-mini
- o4-mini
- gpt-5.1-chat
- codex-mini

## 📝 最佳实践

### 1. 选择合适的模型

**对话应用**:
- gpt-5-chat ✅
- gpt-5.2-chat ✅
- gpt-4o ✅
- gpt-35-turbo ✅

**代码生成**:
- gpt-5.2-codex ✅
- gpt-5.1-codex (需 Responses API) ⚠️
- codex-mini (需 Responses API) ⚠️

**推理和数学**:
- o4-mini ✅
- o3-mini ✅
- o1 ✅

**经济实惠**:
- gpt-5-nano ✅
- gpt-5-mini ✅
- gpt-4o-mini ✅
- gpt-35-turbo ✅

### 2. 部署前检查

✅ **部署检查清单**:
1. 模型是否支持 Chat Completions API？
2. 模型是否需要申请访问？
3. 当前区域是否支持该模型？
4. 是否有足够的配额？

### 3. 代码实现建议

```python
# ✅ 好的做法：检查模型类型并使用正确的 API
def call_model(client, model, messages):
    # 仅支持 Responses API 的模型
    responses_api_only = [
        "gpt-5-pro", 
        "gpt-5.1-codex", 
        "gpt-5.1-codex-mini",
        "codex-mini"
    ]
    
    # 推理模型（不支持 temperature）
    reasoning_models = [
        "o1", "o1-mini", 
        "o3-mini", "o4-mini",
        "gpt-5.1-chat", "codex-mini"
    ]
    
    if model in responses_api_only:
        # 使用 Responses API
        return client.responses.create(model=model, messages=messages)
    elif model in reasoning_models:
        # 不使用 temperature
        return client.chat.completions.create(
            model=model,
            messages=messages
        )
    else:
        # 标准调用
        return client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
```

### 4. 错误处理

```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    error_msg = str(e)
    
    if "OperationNotSupported" in error_msg:
        print("该模型不支持 Chat Completions API")
        print("请使用 Responses API 或选择其他模型")
    elif "DeploymentNotFound" in error_msg:
        print("模型未部署，请在 Azure OpenAI Studio 中部署")
    elif "invalid_request_error" in error_msg:
        print("参数错误，检查 temperature 等参数")
```

## 🔗 相关资源

### 官方文档
- **Azure OpenAI 模型**: https://learn.microsoft.com/azure/ai-foundry/foundry-models/
- **Chat Completions API**: https://learn.microsoft.com/azure/ai-foundry/openai/how-to/chatgpt
- **Responses API**: https://learn.microsoft.com/azure/ai-foundry/openai/how-to/responses
- **推理模型**: https://learn.microsoft.com/azure/ai-foundry/openai/how-to/reasoning

### 申请访问
- **GPT-5 系列**: https://aka.ms/oai/gpt5access
- **GPT-Image 系列**: https://aka.ms/oai/gptimage1access

### Azure Portal
- **Azure OpenAI Studio**: https://oai.azure.com
- **Azure Portal**: https://portal.azure.com

## 💡 常见问题

### Q: 如何知道我的模型支持哪些 API？
A: 查看本文档的兼容性表格，或访问 Azure OpenAI Studio 查看模型详情。

### Q: 为什么我的模型调用失败？
A: 常见原因：
1. 模型不支持该 API
2. 模型未部署
3. 使用了不支持的参数（如推理模型的 temperature）
4. API Key 无效或配额不足

### Q: 如何申请访问受限模型？
A: 访问相应的申请链接，填写表单说明使用场景，等待审批。

### Q: 不同模型的成本如何？
A: 访问 Azure OpenAI 定价页面查看详细信息：
https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/

---

**文档版本**: 1.0  
**最后更新**: 2026-01-16  
**基于**: Azure OpenAI 官方文档
