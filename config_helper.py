import streamlit as st
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置页面
st.set_page_config(
    page_title="Azure OpenAI 配置助手",
    page_icon="⚙️",
    layout="centered"
)

st.title("⚙️ Azure OpenAI 配置助手")

st.markdown("""
这个工具帮助你测试 Azure OpenAI API 配置是否正确。
""")

# 配置表单
with st.form("config_form"):
    st.subheader("API 配置")
    
    api_key = st.text_input(
        "API Key",
        value=os.getenv("AZURE_OPENAI_API_KEY", ""),
        type="password",
        help="你的 Azure OpenAI API 密钥"
    )
    
    api_base = st.text_input(
        "API Base URL",
        value=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        placeholder="https://your-resource.openai.azure.com/",
        help="Azure OpenAI 端点 URL"
    )
    
    api_version = st.text_input(
        "API Version",
        value=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        help="API 版本"
    )
    
    test_model = st.text_input(
        "测试模型名称",
        value="gpt-4.1-nano",
        help="用于测试的模型部署名称"
    )
    
    submitted = st.form_submit_button("🧪 测试连接", type="primary")

if submitted:
    if not api_key or not api_base:
        st.error("❌ 请填写 API Key 和 API Base URL")
    else:
        with st.spinner("正在测试连接..."):
            try:
                # 初始化客户端
                client = AzureOpenAI(
                    api_key=api_key,
                    api_version=api_version,
                    azure_endpoint=api_base
                )
                
                # 测试调用
                response = client.chat.completions.create(
                    model=test_model,
                    messages=[
                        {"role": "user", "content": "Say 'Hello, Azure OpenAI!'"}
                    ],
                    max_tokens=50
                )
                
                st.success("✅ 连接成功！")
                st.markdown("### 📤 测试响应")
                st.info(response.choices[0].message.content)
                
                st.markdown("### 📊 响应详情")
                col1, col2, col3 = st.columns(3)
                col1.metric("模型", response.model)
                col2.metric("输入 Tokens", response.usage.prompt_tokens)
                col3.metric("输出 Tokens", response.usage.completion_tokens)
                
                st.markdown("### 💾 保存配置")
                st.markdown("""
                你可以将配置保存到 `.env` 文件中：
                
                ```env
                AZURE_OPENAI_API_KEY={api_key}
                AZURE_OPENAI_ENDPOINT={api_base}
                AZURE_OPENAI_API_VERSION={api_version}
                ```
                """.format(api_key="***" * 10, api_base=api_base, api_version=api_version))
                
                st.success("✅ 配置验证通过！现在可以使用主应用了。")
                
            except Exception as e:
                st.error(f"❌ 连接失败: {str(e)}")
                
                st.markdown("### 🔍 常见问题")
                st.markdown("""
                1. **认证错误**: 检查 API Key 是否正确
                2. **端点错误**: 确保 URL 格式正确（以 `/` 结尾）
                3. **模型不存在**: 确认模型部署名称正确
                4. **配额限制**: 检查 Azure 订阅是否有足够配额
                """)

st.divider()

st.markdown("""
### 📚 使用说明

1. **获取 API Key**: 
   - 登录 [Azure Portal](https://portal.azure.com)
   - 找到你的 Azure OpenAI 资源
   - 在"密钥和终结点"页面获取

2. **API Base URL 格式**:
   - 格式: `https://<resource-name>.openai.azure.com/`
   - 确保以 `/` 结尾

3. **模型部署**:
   - 确保已在 Azure OpenAI Studio 中部署模型
   - 使用部署名称（不是模型名称）

4. **测试成功后**:
   - 运行主应用: `streamlit run app.py`
   - 或保存配置到 `.env` 文件
""")
