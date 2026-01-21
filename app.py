"""
Azure OpenAI 模型测试门户 - 主页面
"""

import streamlit as st
from pathlib import Path

# 添加 lib 和 utils 到路径
import sys
sys.path.insert(0, str(Path(__file__).parent))

from lib.config_manager import ConfigManager
from lib.models import AVAILABLE_MODELS
from utils.styles import CUSTOM_CSS

# 页面配置
st.set_page_config(
    page_title="Azure OpenAI 模型测试门户",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用自定义样式
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 初始化配置管理器
config_manager = ConfigManager()

# 初始化 session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'api_base' not in st.session_state:
    st.session_state.api_base = ""
if 'api_version' not in st.session_state:
    st.session_state.api_version = "2024-02-15-preview"
if 'use_config_file' not in st.session_state:
    st.session_state.use_config_file = False
if 'selected_config_id' not in st.session_state:
    st.session_state.selected_config_id = None

# 主页面内容
def main():
    st.markdown('<div class="main-header">🤖 Azure OpenAI 模型测试门户</div>', unsafe_allow_html=True)
    
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 配置")
        
        # 配置模式选择
        st.subheader("📂 配置模式")
        use_config_file = st.radio(
            "选择配置方式",
            options=[False, True],
            format_func=lambda x: "📝 手动输入" if not x else "📁 从配置文件加载",
            key="config_mode_radio"
        )
        st.session_state.use_config_file = use_config_file
        
        st.divider()
        
        # 根据配置模式显示不同的UI
        if use_config_file:
            # 从配置文件加载
            st.subheader("📁 配置文件")
            model_configs = config_manager.load_configs()
            
            if not model_configs:
                st.warning("⚠️ 配置文件为空或不存在")
                st.info("请先在 [模型配置管理](/1_🔧_模型配置管理) 页面添加配置")
                selected_model = None
                api_key = ""
                api_base = ""
                api_version = "2024-02-15-preview"
                reasoning_enabled = False
                reasoning_effort = "none"
            else:
                # 创建配置选择器
                config_options = {
                    f"{c['id']}": f"{c['model_name']} - {c.get('description', 'No description')}"
                    for c in model_configs
                }
                
                selected_config_key = st.selectbox(
                    "选择配置",
                    options=list(config_options.keys()),
                    format_func=lambda x: config_options[x]
                )
                
                # 获取选中的配置
                selected_config = config_manager.get_config_by_id(
                    model_configs, 
                    int(selected_config_key)
                )
                
                if selected_config:
                    st.session_state.selected_config_id = selected_config['id']
                    selected_model = selected_config['model_name']
                    api_key = selected_config['api_key']
                    api_base = selected_config['endpoint']
                    api_version = selected_config.get('api_version', '2024-02-15-preview')
                    reasoning_enabled = selected_config.get('reasoning_enabled', False)
                    reasoning_effort = selected_config.get('reasoning_effort', 'none')
                    
                    # 显示配置信息
                    with st.expander("📋 配置详情", expanded=True):
                        st.write(f"**模型**: {selected_model}")
                        st.write(f"**Endpoint**: {api_base}")
                        st.write(f"**API Version**: {api_version}")
                        if reasoning_enabled:
                            st.write(f"**推理模式**: ✅ 启用 ({reasoning_effort})")
                        else:
                            st.write(f"**推理模式**: ❌ 未启用")
                else:
                    selected_model = None
                    api_key = ""
                    api_base = ""
                    api_version = "2024-02-15-preview"
                    reasoning_enabled = False
                    reasoning_effort = "none"
        else:
            # 手动输入模式
            st.subheader("API 设置")
            api_key = st.text_input("API Key", type="password", value=st.session_state.api_key)
            api_base = st.text_input("API Base URL", value=st.session_state.api_base, 
                                     placeholder="https://your-resource.openai.azure.com/")
            api_version = st.text_input("API Version", value=st.session_state.api_version)
            
            if st.button("💾 保存配置"):
                st.session_state.api_key = api_key
                st.session_state.api_base = api_base
                st.session_state.api_version = api_version
                st.success("配置已保存！")
            
            st.divider()
            
            # 模型选择
            st.subheader("🎯 模型选择")
            
            model_family = st.selectbox(
                "模型系列",
                options=list(AVAILABLE_MODELS.keys())
            )
            
            model_options = AVAILABLE_MODELS[model_family]["models"]
            model_name = st.selectbox(
                "具体模型",
                options=list(model_options.keys()),
                format_func=lambda x: f"{x} - {model_options[x]['desc']}"
            )
            
            selected_model_info = model_options[model_name]
            selected_model = selected_model_info["name"]
            api_type = selected_model_info["api"]
            
            st.info(f"**当前选择**: {selected_model}")
            
            # API 支持提示
            if "Responses API Only" in api_type:
                st.warning(f"⚠️ **注意**: {selected_model} 仅支持 Responses API")
            elif "需注册" in selected_model_info["desc"]:
                st.warning(f"⚠️ **注意**: {selected_model} 需要申请注册")
            
            reasoning_enabled = False
            reasoning_effort = "none"
        
        st.divider()
        
        # 参数配置
        st.subheader("🔧 参数设置")
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100)
        top_p = st.slider("Top P", 0.0, 1.0, 0.95, 0.05)
        stream_output = st.checkbox("流式输出", value=False)
        
        st.divider()
        
        # 清空对话历史
        if st.button("🗑️ 清空对话历史"):
            st.session_state.chat_history = []
            st.rerun()
    
    # 主内容区域 - Tab 布局
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 聊天测试", 
        "📝 单次调用", 
        "📊 批量测试", 
        "📖 模型信息"
    ])
    
    with tab1:
        st.header("💬 聊天模式测试")
        st.info("在下方输入消息进行多轮对话测试")
        
        # 显示对话历史
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                st.chat_message(message["role"]).write(message["content"])
        
        # 用户输入
        if prompt := st.chat_input("输入你的消息..."):
            if not api_key or not api_base:
                st.error("❌ 请先配置 API Key 和 API Base URL")
            elif not selected_model:
                st.error("❌ 请选择一个模型")
            else:
                # 显示用户消息
                st.chat_message("user").write(prompt)
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                # 调用 API
                from lib.api_client import AzureOpenAIClient
                from utils.ui_components import display_error, display_metrics
                
                try:
                    client = AzureOpenAIClient(api_key, api_base, api_version)
                    
                    messages = [{"role": m["role"], "content": m["content"]} 
                               for m in st.session_state.chat_history]
                    
                    with st.spinner("正在生成回复..."):
                        response, result = client.chat_completion(
                            model=selected_model,
                            messages=messages,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            top_p=top_p,
                            stream=stream_output,
                            reasoning_effort=reasoning_effort if use_config_file else None
                        )
                        
                        if response:
                            if stream_output:
                                # 流式输出
                                response_placeholder = st.empty()
                                full_response = ""
                                for chunk in response:
                                    if chunk.choices[0].delta.content:
                                        full_response += chunk.choices[0].delta.content
                                        response_placeholder.chat_message("assistant").write(full_response)
                                assistant_message = full_response
                            else:
                                # 非流式输出
                                assistant_message = response.choices[0].message.content
                                st.chat_message("assistant").write(assistant_message)
                                
                                # 显示指标
                                if result:
                                    display_metrics(result)
                            
                            # 保存助手消息
                            st.session_state.chat_history.append({
                                "role": "assistant", 
                                "content": assistant_message
                            })
                        else:
                            # 显示错误
                            display_error(result)
                
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
    
    with tab2:
        st.header("📝 单次 API 调用测试")
        st.info("测试单个 API 请求和响应")
        
        col1, col2 = st.columns(2)
        
        with col1:
            system_prompt = st.text_area(
                "System Prompt (可选)",
                placeholder="你是一个有帮助的AI助手...",
                height=100
            )
        
        with col2:
            user_prompt = st.text_area(
                "User Prompt *",
                placeholder="输入你的问题或提示...",
                height=100
            )
        
        if st.button("🚀 发送请求", type="primary", use_container_width=True):
            if not user_prompt:
                st.warning("⚠️ 请输入 User Prompt")
            elif not api_key or not api_base:
                st.error("❌ 请先配置 API Key 和 API Base URL")
            elif not selected_model:
                st.error("❌ 请选择一个模型")
            else:
                from lib.api_client import AzureOpenAIClient
                from utils.ui_components import display_error, display_metrics
                
                try:
                    client = AzureOpenAIClient(api_key, api_base, api_version)
                    
                    messages = []
                    if system_prompt:
                        messages.append({"role": "system", "content": system_prompt})
                    messages.append({"role": "user", "content": user_prompt})
                    
                    with st.spinner("正在调用 API..."):
                        response, result = client.chat_completion(
                            model=selected_model,
                            messages=messages,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            top_p=top_p,
                            reasoning_effort=reasoning_effort if use_config_file else None
                        )
                        
                        if response:
                            st.success("✅ 调用成功！")
                            
                            # 显示响应
                            st.markdown("### 📤 响应内容")
                            st.markdown(
                                f'<div class="response-box">{response.choices[0].message.content}</div>', 
                                unsafe_allow_html=True
                            )
                            
                            # 显示指标
                            if result:
                                st.markdown("### 📊 性能指标")
                                display_metrics(result)
                        else:
                            display_error(result)
                
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
    
    with tab3:
        st.header("📊 批量测试工具")
        st.info("批量测试多个用例")
        
        st.markdown("**功能开发中...**")
    
    with tab4:
        st.header("📖 模型信息")
        
        for family_name, family_data in AVAILABLE_MODELS.items():
            st.subheader(family_name)
            
            for model_key, model_info in family_data["models"].items():
                with st.expander(f"🤖 {model_info['name']}"):
                    st.write(f"**API 支持**: {model_info['api']}")
                    st.write(f"**描述**: {model_info['desc']}")

if __name__ == "__main__":
    main()
