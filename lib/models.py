"""
模型定义和配置
"""

# 可用模型列表和API支持信息
AVAILABLE_MODELS = {
    "GPT-4.1 系列": {
        "models": {
            "gpt-4.1": {"name": "gpt-4.1", "api": "Chat Completions", "desc": "标准版本"},
            "gpt-4.1-nano": {"name": "gpt-4.1-nano", "api": "Chat Completions", "desc": "轻量快速版"},
            "gpt-4.1-mini": {"name": "gpt-4.1-mini", "api": "Chat Completions", "desc": "迷你版本"},
        }
    },
    "GPT-5 系列": {
        "models": {
            "gpt-5": {"name": "gpt-5", "api": "Chat Completions", "desc": "标准版本 (需注册)"},
            "gpt-5-mini": {"name": "gpt-5-mini", "api": "Chat Completions", "desc": "迷你版本"},
            "gpt-5-nano": {"name": "gpt-5-nano", "api": "Chat Completions", "desc": "纳米版本"},
            "gpt-5-chat": {"name": "gpt-5-chat", "api": "Chat Completions", "desc": "对话优化版"},
            "gpt-5-pro": {"name": "gpt-5-pro", "api": "Responses API Only", "desc": "专业版 (需注册)"},
        }
    },
    "GPT-5.1 系列": {
        "models": {
            "gpt-5.1": {"name": "gpt-5.1", "api": "Chat Completions", "desc": "标准版本 (需注册)"},
            "gpt-5.1-chat": {"name": "gpt-5.1-chat", "api": "Chat Completions", "desc": "对话版本 (Preview)"},
        }
    },
    "GPT-5.2 系列": {
        "models": {
            "gpt-5.2": {"name": "gpt-5.2", "api": "Chat Completions", "desc": "标准版本 (需注册)"},
            "gpt-5.2-chat": {"name": "gpt-5.2-chat", "api": "Chat Completions", "desc": "对话版本 (Preview)"},
            "gpt-5.2-codex": {"name": "gpt-5.2-codex", "api": "Chat Completions", "desc": "代码优化版 (需注册)"},
        }
    },
    "GPT-4o 系列": {
        "models": {
            "gpt-4o": {"name": "gpt-4o", "api": "Chat Completions", "desc": "GPT-4 Omni 标准版"},
            "gpt-4o-mini": {"name": "gpt-4o-mini", "api": "Chat Completions", "desc": "GPT-4 Omni 迷你版"},
        }
    },
    "GPT-4 Turbo": {
        "models": {
            "gpt-4-turbo": {"name": "gpt-4", "api": "Chat Completions", "desc": "GPT-4 Turbo"},
        }
    },
    "GPT-3.5 系列": {
        "models": {
            "gpt-35-turbo": {"name": "gpt-35-turbo", "api": "Chat Completions", "desc": "GPT-3.5 Turbo"},
        }
    },
    "o 系列 (推理模型)": {
        "models": {
            "o1": {"name": "o1", "api": "Chat Completions", "desc": "推理模型"},
            "o1-mini": {"name": "o1-mini", "api": "Chat Completions", "desc": "推理模型迷你版"},
            "o3-mini": {"name": "o3-mini", "api": "Chat Completions", "desc": "推理模型 o3-mini"},
        }
    },
    "Grok 系列": {
        "models": {
            "grok-4-fast-non-reasoning": {"name": "grok-4-fast-non-reasoning", "api": "Chat Completions", "desc": "快速推理版本"},
        }
    }
}

# 支持推理的模型列表
REASONING_SUPPORTED_MODELS = [
    "gpt-5", "gpt-5-mini", "gpt-5-nano", "gpt-5-chat", "gpt-5-pro",
    "gpt-5.1", "gpt-5.1-chat",
    "gpt-5.2", "gpt-5.2-chat", "gpt-5.2-codex",
    "o1", "o1-mini", "o3-mini"
]

# 推理级别选项
REASONING_EFFORTS = {
    "none": "无推理（标准响应）",
    "minimal": "最小推理",
    "low": "低推理",
    "medium": "中等推理",
    "high": "高推理"
}

# 推理级别说明
REASONING_HELP = """
**推理级别说明：**
- **none**: 标准响应，不使用推理能力
- **minimal**: 最小推理，适合简单任务
- **low**: 低推理，适合一般任务
- **medium**: 中等推理，适合复杂任务
- **high**: 高推理，适合需要深度思考的任务

⚠️ **注意**: 只有 GPT-5 系列和 o 系列模型支持推理参数
"""
