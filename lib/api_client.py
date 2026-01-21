"""
Azure OpenAI API 客户端模块
负责 API 调用和错误处理
"""

import time
from openai import AzureOpenAI
from typing import Dict, Tuple, Optional, Any


class AzureOpenAIClient:
    """Azure OpenAI API 客户端"""
    
    def __init__(self, api_key: str, endpoint: str, api_version: str):
        """初始化客户端"""
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
    
    def chat_completion(
        self,
        model: str,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        top_p: float = 0.95,
        stream: bool = False,
        reasoning_effort: Optional[str] = None
    ) -> Tuple[Any, Optional[Dict]]:
        """
        调用聊天完成 API
        
        Returns:
            (response, metrics) 如果成功
            (None, error_dict) 如果失败
        """
        try:
            start_time = time.time()
            
            # 构建请求参数
            request_params = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "stream": stream
            }
            
            # 添加推理参数
            if reasoning_effort and reasoning_effort != "none":
                request_params["reasoning_effort"] = reasoning_effort
            
            response = self.client.chat.completions.create(**request_params)
            
            if stream:
                return response, None
            else:
                end_time = time.time()
                latency = end_time - start_time
                
                metrics = {
                    "latency": latency,
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
                
                return response, metrics
                
        except Exception as e:
            error_info = self._parse_error(str(e), model)
            return None, error_info
    
    def _parse_error(self, error_msg: str, model: str) -> Dict:
        """解析错误信息"""
        error_dict = {
            "error": True,
            "message": error_msg,
            "model": model
        }
        
        if "OperationNotSupported" in error_msg:
            error_dict["type"] = "OperationNotSupported"
            error_dict["title"] = "API 不支持错误"
            error_dict["description"] = f"模型 `{model}` 不支持 Chat Completions API"
            error_dict["solutions"] = [
                "检查该模型是否需要使用 Responses API",
                "选择其他支持 Chat Completions API 的模型",
                "参考文档: https://learn.microsoft.com/azure/ai-foundry/openai/"
            ]
        elif "DeploymentNotFound" in error_msg:
            error_dict["type"] = "DeploymentNotFound"
            error_dict["title"] = "部署未找到"
            error_dict["description"] = f"模型 `{model}` 未在您的 Azure OpenAI 资源中部署"
            error_dict["solutions"] = [
                "在 Azure OpenAI Studio 中部署该模型",
                "确保使用的是部署名称而不是模型名称",
                "检查部署是否在正确的区域"
            ]
        elif "invalid_request_error" in error_msg:
            error_dict["type"] = "InvalidRequest"
            error_dict["title"] = "请求参数错误"
            error_dict["description"] = error_msg
            error_dict["solutions"] = [
                "检查 Temperature 等参数是否在有效范围内",
                "检查 Max Tokens 设置是否合理",
                "某些推理模型不支持 temperature 参数"
            ]
        elif "401" in error_msg or "Unauthorized" in error_msg:
            error_dict["type"] = "Unauthorized"
            error_dict["title"] = "认证失败"
            error_dict["description"] = "API Key 无效或已过期"
            error_dict["solutions"] = [
                "检查 API Key 是否正确",
                "确认 API Key 未过期",
                "在 Azure Portal 中重新生成密钥"
            ]
        elif "429" in error_msg or "RateLimitReached" in error_msg:
            error_dict["type"] = "RateLimit"
            error_dict["title"] = "速率限制"
            error_dict["description"] = "请求频率过高或配额已用完"
            error_dict["solutions"] = [
                "等待几秒后重试",
                "检查 Azure 订阅配额",
                "考虑升级配额或使用不同的区域"
            ]
        else:
            error_dict["type"] = "Unknown"
            error_dict["title"] = "API 调用失败"
            error_dict["description"] = error_msg
            error_dict["solutions"] = ["检查网络连接", "查看详细错误信息"]
        
        return error_dict
    
    def test_connection(self, model: str, reasoning_effort: Optional[str] = None) -> Tuple[bool, str]:
        """测试连接"""
        messages = [{"role": "user", "content": "Hello, this is a test."}]
        
        response, result = self.chat_completion(
            model=model,
            messages=messages,
            max_tokens=10,
            reasoning_effort=reasoning_effort
        )
        
        if response:
            return True, "✅ 连接成功！模型响应正常。"
        else:
            return False, f"❌ 连接失败: {result.get('description', '未知错误')}"
