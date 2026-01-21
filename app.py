"""
Azure OpenAI 聊天测试
简单的聊天界面，用于测试 GPT 模型
"""

import streamlit as st
from openai import AzureOpenAI
import json
from pathlib import Path

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

# 初始化 session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'config' not in st.session_state:
    st.session_state.config = load_config()

# 标题
st.title("💬 GPT 聊天测试")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")
    
    # API 配置
    api_key = st.text_input(
        "API Key", 
        type="password", 
        value=st.session_state.config.get('api_key', ''),
        key="api_key"
    )
    endpoint = st.text_input(
        "Endpoint", 
        placeholder="https://your-resource.openai.azure.com/",
        value=st.session_state.config.get('endpoint', ''),
        key="endpoint"
    )
    model = st.text_input(
        "模型名称", 
        value=st.session_state.config.get('model', 'gpt-4'),
        key="model"
    )
    api_version = st.text_input(
        "API Version", 
        value=st.session_state.config.get('api_version', '2024-02-15-preview'),
        key="api_version"
    )
    
    # 保存配置按钮
    if st.button("💾 保存配置", use_container_width=True):
        config = {
            'api_key': api_key,
            'endpoint': endpoint,
            'model': model,
            'api_version': api_version
        }
        if save_config(config):
            st.session_state.config = config
            st.success("✅ 配置已保存！")
        else:
            st.error("❌ 保存失败")
    
    st.divider()
    
    # 参数设置
    st.subheader("🔧 参数")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max Completion Tokens", 100, 4000, 1000, 100)
    
    st.divider()
    
    # 清空按钮
    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 显示对话历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 用户输入
if prompt := st.chat_input("输入你的消息..."):
    # 检查配置
    if not api_key or not endpoint:
        st.error("❌ 请先在侧边栏配置 API Key 和 Endpoint")
    else:
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # 调用 API
        try:
            client = AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=endpoint
            )
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # 流式输出 - 使用 max_completion_tokens 而不是 max_tokens
                for response in client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                    temperature=temperature,
                    max_completion_tokens=max_tokens,  # 改用 max_completion_tokens
                    stream=True
                ):
                    if response.choices[0].delta.content:
                        full_response += response.choices[0].delta.content
                        message_placeholder.write(full_response)
                
                # 保存助手消息
                st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        except Exception as e:
            st.error(f"❌ 错误: {str(e)}")
