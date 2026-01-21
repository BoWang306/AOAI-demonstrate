"""
Azure OpenAI 聊天测试
支持文本和图片输入，使用 Responses API
"""

import streamlit as st
from openai import OpenAI
import json
from pathlib import Path
import base64
import time
from io import BytesIO
from PIL import Image

# 页面配置
st.set_page_config(
    page_title="GPT 聊天测试",
    page_icon="💬",
    layout="wide"
)

# 配置文件路径
CONFIG_FILE = Path("config.json")

# 加载配置
def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

# 保存配置
def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

# 编码图片为 base64
def encode_image(image_file):
    """将上传的图片文件编码为 base64 URL"""
    try:
        # 读取图片
        image = Image.open(image_file)
        # 转换为 RGB（如果是 RGBA）
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        # 保存到字节流
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()
        
        # 编码为 base64
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return f"data:image/jpeg;base64,{img_base64}"
    except Exception as e:
        st.error(f"图片编码失败: {str(e)}")
        return None

# 初始化 session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'config' not in st.session_state:
    st.session_state.config = load_config()

# 标题
st.title("💬 GPT 聊天测试")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 聊天模型配置")
    
    # 从配置文件加载聊天模型的配置
    chat_config = st.session_state.config.get('chat', {})
    
    # API 配置
    api_key = st.text_input(
        "API Key", 
        type="password", 
        value=chat_config.get('api_key', ''),
        key="chat_api_key"
    )
    endpoint = st.text_input(
        "Endpoint (Base URL)", 
        placeholder="https://your-resource.openai.azure.com/openai/deployments/your-model",
        value=chat_config.get('endpoint', ''),
        key="chat_endpoint",
        help="完整的部署 URL"
    )
    model = st.text_input(
        "模型名称", 
        value=chat_config.get('model', 'gpt-4o'),
        key="chat_model"
    )
    
    # 保存配置按钮
    if st.button("💾 保存聊天配置", use_container_width=True):
        config = st.session_state.config
        config['chat'] = {
            'api_key': api_key,
            'endpoint': endpoint,
            'model': model
        }
        if save_config(config):
            st.session_state.config = config
            st.success("✅ 聊天配置已保存！")
        else:
            st.error("❌ 保存失败")
    
    st.divider()
    
    # 参数设置
    st.subheader("🔧 参数")
    
    # Reasoning effort
    reasoning_effort = st.selectbox(
        "Reasoning Effort",
        options=["none", "minimal", "low", "medium", "high"],
        index=0,
        help="推理级别（仅支持 GPT-5 系列和 o 系列）"
    )
    
    st.divider()
    
    # 清空按钮
    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 显示对话历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # 显示文本
        if "text" in message:
            st.write(message["text"])
        
        # 显示图片
        if "image" in message:
            st.image(message["image"], width=300)

# 图片上传
uploaded_file = st.file_uploader("📎 上传图片（可选）", type=['png', 'jpg', 'jpeg'], key="image_upload")

# 用户输入
if prompt := st.chat_input("输入你的消息..."):
    # 检查配置
    if not api_key or not endpoint:
        st.error("❌ 请先在侧边栏配置 API Key 和 Endpoint")
    else:
        # 构造用户消息
        user_message = {"role": "user", "text": prompt}
        
        # 处理图片
        image_data = None
        if uploaded_file is not None:
            image_data = encode_image(uploaded_file)
            if image_data:
                user_message["image"] = uploaded_file
        
        # 添加用户消息
        st.session_state.messages.append(user_message)
        
        # 显示用户消息
        with st.chat_message("user"):
            st.write(prompt)
            if uploaded_file is not None and image_data:
                st.image(uploaded_file, width=300)
        
        # 调用 API
        try:
            # 初始化客户端
            client = OpenAI(
                base_url=endpoint,
                api_key=api_key,
            )
            
            # 构造 input（使用 Responses API 格式）
            content = [
                {
                    "type": "input_text",
                    "text": prompt
                }
            ]
            
            # 如果有图片，添加到 content
            if image_data:
                content.append({
                    "type": "input_image",
                    "image_url": image_data
                })
            
            input_items = [
                {
                    "type": "message",
                    "role": "user",
                    "content": content
                }
            ]
            
            # 显示助手消息
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                metrics_placeholder = st.empty()
                
                full_response = ""
                first_token_time = None
                start_time = time.time()
                reasoning_tokens = 0
                total_tokens = 0
                
                # 流式请求
                reasoning_config = {"effort": reasoning_effort} if reasoning_effort != "none" else None
                
                stream = client.responses.create(
                    model=model,
                    input=input_items,
                    stream=True,
                    reasoning=reasoning_config
                )
                
                # 处理流式事件
                for event in stream:
                    # 捕获文本增量
                    if event.type == "response.output_text.delta":
                        if first_token_time is None:
                            first_token_time = time.time()
                        
                        if hasattr(event, 'delta') and event.delta:
                            full_response += event.delta
                            message_placeholder.write(full_response)
                    
                    # 捕获完成事件，提取 tokens
                    elif event.type == "response.completed":
                        if hasattr(event, 'response') and event.response and hasattr(event.response, 'usage'):
                            usage = event.response.usage
                            
                            # 提取 Total Tokens
                            if hasattr(usage, 'total_tokens'):
                                total_tokens = usage.total_tokens
                            
                            # 提取 Reasoning Tokens
                            if hasattr(usage, 'output_tokens_details') and usage.output_tokens_details:
                                if hasattr(usage.output_tokens_details, 'reasoning_tokens'):
                                    reasoning_tokens = usage.output_tokens_details.reasoning_tokens
                
                end_time = time.time()
                
                # 计算指标
                ttft = (first_token_time - start_time) if first_token_time else 0
                total_duration = end_time - start_time
                
                # 显示指标
                if total_tokens > 0:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("⏱️ TTFT", f"{ttft:.2f}s")
                    with col2:
                        st.metric("⌛ 总时长", f"{total_duration:.2f}s")
                    with col3:
                        st.metric("🧠 Reasoning", reasoning_tokens)
                    with col4:
                        st.metric("📊 Total Tokens", total_tokens)
                
                # 保存助手消息
                st.session_state.messages.append({
                    "role": "assistant", 
                    "text": full_response
                })
        
        except Exception as e:
            st.error(f"❌ 错误: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
