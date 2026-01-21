"""
Azure OpenAI 聊天测试
简单的聊天界面，用于测试 GPT 模型
"""

import streamlit as st
from openai import AzureOpenAI

# 页面配置
st.set_page_config(
    page_title="GPT 聊天测试",
    page_icon="💬",
    layout="wide"
)

# 初始化 session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 标题
st.title("💬 GPT 聊天测试")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")
    
    # API 配置
    api_key = st.text_input("API Key", type="password", key="api_key")
    endpoint = st.text_input("Endpoint", placeholder="https://your-resource.openai.azure.com/", key="endpoint")
    model = st.text_input("模型名称", value="gpt-4", key="model")
    api_version = st.text_input("API Version", value="2024-02-15-preview", key="api_version")
    
    st.divider()
    
    # 参数设置
    st.subheader("🔧 参数")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100)
    
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
                
                # 流式输出
                for response in client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                ):
                    if response.choices[0].delta.content:
                        full_response += response.choices[0].delta.content
                        message_placeholder.write(full_response)
                
                # 保存助手消息
                st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        except Exception as e:
            st.error(f"❌ 错误: {str(e)}")
