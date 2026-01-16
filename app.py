import streamlit as st
import os
from openai import AzureOpenAI
import json
from datetime import datetime
import time

# 页面配置
st.set_page_config(
    page_title="Azure OpenAI 模型测试门户",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0078D4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .model-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .response-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0078D4;
        margin: 1rem 0;
    }
    .metrics-box {
        background-color: #f9f9f9;
        padding: 0.8rem;
        border-radius: 0.3rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 可用模型列表
AVAILABLE_MODELS = {
    "GPT-4.1": {
        "gpt-4.1-nano": "gpt-4.1-nano",
    },
    "GPT-5": {
        "gpt-5": "gpt-5",
        "gpt-5-nano": "gpt-5-nano",
        "gpt-5-pro": "gpt-5-pro",
    },
    "GPT-5.1": {
        "gpt-5.1-chat": "gpt-5.1-chat",
    },
    "GPT-5.2": {
        "gpt-5.2": "gpt-5.2",
        "gpt-5.2-chat": "gpt-5.2-chat",
        "gpt-5.2-chat-2": "gpt-5.2-chat",
        "gpt-5.2-codex": "gpt-5.2-codex",
    },
    "GPT-Realtime": {
        "gpt-realtime": "gpt-realtime",
    },
    "Grok": {
        "grok-4-fast-non-reasoning": "grok-4-fast-non-reasoning",
    }
}

# 初始化 session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'api_base' not in st.session_state:
    st.session_state.api_base = ""
if 'api_version' not in st.session_state:
    st.session_state.api_version = "2024-02-15-preview"

def initialize_client(api_key, api_base, api_version):
    """初始化 Azure OpenAI 客户端"""
    try:
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=api_base
        )
        return client
    except Exception as e:
        st.error(f"客户端初始化失败: {str(e)}")
        return None

def call_chat_completion(client, model, messages, temperature, max_tokens, top_p, stream=False):
    """调用聊天完成 API"""
    try:
        start_time = time.time()
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream
        )
        
        if stream:
            return response, None
        else:
            end_time = time.time()
            latency = end_time - start_time
            
            return response, {
                "latency": latency,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
    except Exception as e:
        st.error(f"API 调用失败: {str(e)}")
        return None, None

def main():
    # 页面标题
    st.markdown('<div class="main-header">🤖 Azure OpenAI 模型测试门户</div>', unsafe_allow_html=True)
    
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 配置")
        
        # API 配置
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
        
        model_name = st.selectbox(
            "具体模型",
            options=list(AVAILABLE_MODELS[model_family].keys())
        )
        
        selected_model = AVAILABLE_MODELS[model_family][model_name]
        
        st.info(f"当前选择: **{selected_model}**")
        
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
    
    # 主要内容区域
    tab1, tab2, tab3, tab4 = st.tabs(["💬 聊天测试", "📝 单次调用", "📊 批量测试", "📖 模型信息"])
    
    # Tab 1: 聊天测试
    with tab1:
        st.header("聊天模式测试")
        
        # 显示聊天历史
        chat_container = st.container()
        with chat_container:
            for idx, msg in enumerate(st.session_state.chat_history):
                if msg["role"] == "user":
                    st.chat_message("user").write(msg["content"])
                else:
                    st.chat_message("assistant").write(msg["content"])
        
        # 用户输入
        user_input = st.chat_input("输入您的消息...")
        
        if user_input:
            if not st.session_state.api_key or not st.session_state.api_base:
                st.error("❌ 请先在侧边栏配置 API Key 和 Base URL")
            else:
                # 添加用户消息到历史
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_input
                })
                
                # 显示用户消息
                st.chat_message("user").write(user_input)
                
                # 准备消息列表
                messages = [{"role": msg["role"], "content": msg["content"]} 
                           for msg in st.session_state.chat_history]
                
                # 初始化客户端
                client = initialize_client(
                    st.session_state.api_key,
                    st.session_state.api_base,
                    st.session_state.api_version
                )
                
                if client:
                    with st.spinner("正在生成回复..."):
                        response, metrics = call_chat_completion(
                            client, selected_model, messages,
                            temperature, max_tokens, top_p, stream_output
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
                                if metrics:
                                    col1, col2, col3, col4 = st.columns(4)
                                    col1.metric("延迟", f"{metrics['latency']:.2f}s")
                                    col2.metric("输入 Tokens", metrics['prompt_tokens'])
                                    col3.metric("输出 Tokens", metrics['completion_tokens'])
                                    col4.metric("总计 Tokens", metrics['total_tokens'])
                            
                            # 添加助手消息到历史
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": assistant_message
                            })
                            
                            st.rerun()
    
    # Tab 2: 单次调用
    with tab2:
        st.header("单次 API 调用测试")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            system_prompt = st.text_area("System Prompt (可选)", 
                                        placeholder="你是一个有帮助的AI助手...",
                                        height=100)
            user_prompt = st.text_area("User Prompt", 
                                      placeholder="输入你的问题或指令...",
                                      height=200)
            
            if st.button("🚀 发送请求", type="primary"):
                if not st.session_state.api_key or not st.session_state.api_base:
                    st.error("❌ 请先在侧边栏配置 API Key 和 Base URL")
                elif not user_prompt:
                    st.warning("⚠️ 请输入 User Prompt")
                else:
                    messages = []
                    if system_prompt:
                        messages.append({"role": "system", "content": system_prompt})
                    messages.append({"role": "user", "content": user_prompt})
                    
                    client = initialize_client(
                        st.session_state.api_key,
                        st.session_state.api_base,
                        st.session_state.api_version
                    )
                    
                    if client:
                        with st.spinner("正在调用 API..."):
                            response, metrics = call_chat_completion(
                                client, selected_model, messages,
                                temperature, max_tokens, top_p
                            )
                            
                            if response:
                                st.success("✅ 调用成功！")
                                
                                # 显示响应
                                st.markdown("### 📤 响应内容")
                                st.markdown(f'<div class="response-box">{response.choices[0].message.content}</div>', 
                                          unsafe_allow_html=True)
                                
                                # 显示指标
                                if metrics:
                                    st.markdown("### 📊 性能指标")
                                    col1, col2, col3, col4 = st.columns(4)
                                    col1.metric("⏱️ 延迟", f"{metrics['latency']:.2f}s")
                                    col2.metric("📥 输入 Tokens", metrics['prompt_tokens'])
                                    col3.metric("📤 输出 Tokens", metrics['completion_tokens'])
                                    col4.metric("📊 总计 Tokens", metrics['total_tokens'])
                                
                                # 显示完整响应
                                with st.expander("🔍 查看完整响应 JSON"):
                                    st.json(response.model_dump())
        
        with col2:
            st.markdown("### 💡 提示")
            st.info("""
            **使用说明:**
            1. 配置 API 信息
            2. 选择模型
            3. 设置参数
            4. 输入提示词
            5. 点击发送
            
            **最佳实践:**
            - System Prompt 定义角色
            - User Prompt 描述任务
            - 调整参数优化输出
            """)
    
    # Tab 3: 批量测试
    with tab3:
        st.header("批量测试工具")
        
        st.markdown("### 📋 测试用例配置")
        
        # 允许用户上传 JSON 文件或手动输入
        upload_mode = st.radio("输入模式", ["手动输入", "上传 JSON 文件"])
        
        test_cases = []
        
        if upload_mode == "手动输入":
            num_cases = st.number_input("测试用例数量", min_value=1, max_value=10, value=3)
            
            for i in range(num_cases):
                with st.expander(f"测试用例 {i+1}", expanded=(i==0)):
                    case_name = st.text_input(f"用例名称 {i+1}", value=f"Test Case {i+1}", key=f"case_name_{i}")
                    case_prompt = st.text_area(f"Prompt {i+1}", key=f"case_prompt_{i}", height=100)
                    
                    if case_prompt:
                        test_cases.append({
                            "name": case_name,
                            "prompt": case_prompt
                        })
        else:
            uploaded_file = st.file_uploader("上传测试用例 JSON 文件", type=['json'])
            if uploaded_file:
                try:
                    test_cases = json.load(uploaded_file)
                    st.success(f"✅ 成功加载 {len(test_cases)} 个测试用例")
                except Exception as e:
                    st.error(f"❌ JSON 解析失败: {str(e)}")
        
        if st.button("🚀 开始批量测试", type="primary"):
            if not test_cases:
                st.warning("⚠️ 请添加测试用例")
            elif not st.session_state.api_key or not st.session_state.api_base:
                st.error("❌ 请先在侧边栏配置 API Key 和 Base URL")
            else:
                client = initialize_client(
                    st.session_state.api_key,
                    st.session_state.api_base,
                    st.session_state.api_version
                )
                
                if client:
                    results = []
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, case in enumerate(test_cases):
                        status_text.text(f"正在测试: {case['name']} ({idx+1}/{len(test_cases)})")
                        
                        messages = [{"role": "user", "content": case['prompt']}]
                        response, metrics = call_chat_completion(
                            client, selected_model, messages,
                            temperature, max_tokens, top_p
                        )
                        
                        if response:
                            results.append({
                                "name": case['name'],
                                "prompt": case['prompt'],
                                "response": response.choices[0].message.content,
                                "metrics": metrics
                            })
                        
                        progress_bar.progress((idx + 1) / len(test_cases))
                    
                    status_text.text("✅ 测试完成！")
                    
                    # 显示结果
                    st.markdown("### 📊 测试结果")
                    
                    for result in results:
                        with st.expander(f"📝 {result['name']}", expanded=False):
                            st.markdown("**Prompt:**")
                            st.code(result['prompt'])
                            
                            st.markdown("**Response:**")
                            st.markdown(f'<div class="response-box">{result["response"]}</div>', 
                                      unsafe_allow_html=True)
                            
                            if result['metrics']:
                                col1, col2, col3, col4 = st.columns(4)
                                col1.metric("延迟", f"{result['metrics']['latency']:.2f}s")
                                col2.metric("输入", result['metrics']['prompt_tokens'])
                                col3.metric("输出", result['metrics']['completion_tokens'])
                                col4.metric("总计", result['metrics']['total_tokens'])
                    
                    # 汇总统计
                    st.markdown("### 📈 汇总统计")
                    total_latency = sum(r['metrics']['latency'] for r in results if r['metrics'])
                    avg_latency = total_latency / len(results) if results else 0
                    total_tokens = sum(r['metrics']['total_tokens'] for r in results if r['metrics'])
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("平均延迟", f"{avg_latency:.2f}s")
                    col2.metric("总 Tokens", total_tokens)
                    col3.metric("成功率", f"{len(results)}/{len(test_cases)}")
                    
                    # 导出结果
                    if st.button("💾 导出结果"):
                        result_json = json.dumps(results, ensure_ascii=False, indent=2)
                        st.download_button(
                            label="下载 JSON",
                            data=result_json,
                            file_name=f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
    
    # Tab 4: 模型信息
    with tab4:
        st.header("📖 可用模型列表")
        
        for family, models in AVAILABLE_MODELS.items():
            with st.expander(f"📦 {family}", expanded=True):
                for name, model_id in models.items():
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"**{name}**")
                    with col2:
                        st.code(model_id)
        
        st.divider()
        
        st.markdown("### 📚 使用指南")
        st.markdown("""
        #### 🎯 快速开始
        1. 在侧边栏配置 Azure OpenAI API 信息
        2. 选择要测试的模型
        3. 调整模型参数（Temperature、Max Tokens 等）
        4. 选择测试模式开始使用
        
        #### 💬 聊天测试
        - 支持多轮对话
        - 保留对话历史
        - 实时交互测试
        
        #### 📝 单次调用
        - 快速测试单个请求
        - 查看详细响应和性能指标
        - 支持自定义 System Prompt
        
        #### 📊 批量测试
        - 同时测试多个用例
        - 对比不同输入的输出
        - 导出测试结果
        
        #### ⚙️ 参数说明
        - **Temperature**: 控制输出随机性 (0-2)
        - **Max Tokens**: 最大输出长度
        - **Top P**: 核采样参数 (0-1)
        - **Stream**: 启用流式输出
        
        #### 🔐 安全提示
        - API Key 仅保存在当前会话
        - 不会上传到任何服务器
        - 建议使用环境变量配置敏感信息
        """)

if __name__ == "__main__":
    main()
