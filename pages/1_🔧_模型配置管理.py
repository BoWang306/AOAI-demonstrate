"""
Azure OpenAI 模型配置管理页面
支持添加、编辑、删除和测试多个模型配置
"""

import streamlit as st
import json
import os
from pathlib import Path
from openai import AzureOpenAI
from datetime import datetime
import re

# 页面配置
st.set_page_config(
    page_title="模型配置管理 - Azure OpenAI",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS
st.markdown("""
<style>
    .config-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
        background-color: #f8f9fa;
    }
    .config-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #1f77b4;
    }
    .config-field {
        margin-bottom: 0.5rem;
        padding: 0.3rem;
        background-color: white;
        border-radius: 0.3rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.3rem;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.3rem;
        color: #721c24;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.3rem;
        color: #856404;
        margin: 1rem 0;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 配置文件路径
CONFIG_FILE = Path(__file__).parent.parent / "model_configs.json"

# 支持的推理级别
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

# 支持推理的模型列表
REASONING_SUPPORTED_MODELS = [
    "gpt-5", "gpt-5-mini", "gpt-5-nano", "gpt-5-chat", "gpt-5-pro",
    "gpt-5.1", "gpt-5.1-chat",
    "gpt-5.2", "gpt-5.2-chat", "gpt-5.2-codex",
    "o1", "o1-mini", "o3-mini"
]

def load_configs():
    """加载配置文件"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"加载配置文件失败: {str(e)}")
            return []
    return []

def save_configs(configs):
    """保存配置文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(configs, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"保存配置文件失败: {str(e)}")
        return False

def validate_endpoint(endpoint):
    """验证 endpoint 格式"""
    pattern = r'^https?://[a-zA-Z0-9][-a-zA-Z0-9.]*[a-zA-Z0-9]\.(openai\.azure\.com|azure\.com)'
    return bool(re.match(pattern, endpoint))

def validate_api_key(api_key):
    """验证 API key 格式（基本检查）"""
    return bool(api_key and len(api_key) >= 32)

def test_config(config):
    """测试配置是否可用"""
    try:
        client = AzureOpenAI(
            api_key=config['api_key'],
            api_version=config.get('api_version', '2024-02-15-preview'),
            azure_endpoint=config['endpoint']
        )
        
        # 构建测试消息
        messages = [{"role": "user", "content": "Hello, this is a test."}]
        
        # 如果支持推理且启用了推理
        extra_params = {}
        if config.get('reasoning_enabled', False) and config['model_name'] in REASONING_SUPPORTED_MODELS:
            extra_params['reasoning_effort'] = config.get('reasoning_effort', 'low')
        
        # 发送测试请求
        response = client.chat.completions.create(
            model=config['model_name'],
            messages=messages,
            max_tokens=10,
            **extra_params
        )
        
        return True, "✅ 连接成功！模型响应正常。"
    except Exception as e:
        return False, f"❌ 连接失败: {str(e)}"

def get_unique_config_id(configs):
    """生成唯一的配置 ID"""
    if not configs:
        return 1
    return max([c.get('id', 0) for c in configs]) + 1

# 初始化会话状态
if 'editing_config' not in st.session_state:
    st.session_state.editing_config = None
if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False

# 页面标题
st.title("🔧 模型配置管理")
st.markdown("管理多个 Azure OpenAI 模型的配置，包括 endpoint、API key 和推理参数。")

# 侧边栏
with st.sidebar:
    st.header("📋 操作")
    
    if st.button("➕ 添加新配置", use_container_width=True):
        st.session_state.show_add_form = True
        st.session_state.editing_config = None
        st.rerun()
    
    if st.button("🔄 刷新配置列表", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    
    # 导入/导出功能
    st.subheader("📦 导入/导出")
    
    # 导出配置
    configs = load_configs()
    if configs:
        config_json = json.dumps(configs, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 导出配置文件",
            data=config_json,
            file_name=f"model_configs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    # 导入配置
    uploaded_file = st.file_uploader("📤 导入配置文件", type=['json'])
    if uploaded_file is not None:
        try:
            imported_configs = json.load(uploaded_file)
            if isinstance(imported_configs, list):
                if st.button("确认导入", use_container_width=True):
                    if save_configs(imported_configs):
                        st.success("✅ 配置导入成功！")
                        st.rerun()
            else:
                st.error("❌ 配置文件格式错误！")
        except Exception as e:
            st.error(f"❌ 导入失败: {str(e)}")
    
    st.markdown("---")
    st.info(f"📊 当前配置数量: **{len(configs)}**")

# 主内容区域
configs = load_configs()

# 显示添加/编辑表单
if st.session_state.show_add_form or st.session_state.editing_config is not None:
    st.subheader("➕ 添加新配置" if st.session_state.show_add_form else "✏️ 编辑配置")
    
    # 如果是编辑模式，加载现有配置
    if st.session_state.editing_config is not None:
        edit_config = st.session_state.editing_config
    else:
        edit_config = {
            'model_name': '',
            'endpoint': '',
            'api_key': '',
            'api_version': '2024-02-15-preview',
            'reasoning_enabled': False,
            'reasoning_effort': 'low',
            'description': ''
        }
    
    with st.form("config_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            model_name = st.text_input(
                "模型名称 *",
                value=edit_config.get('model_name', ''),
                placeholder="例如: gpt-5.2",
                help="Azure OpenAI 部署的模型名称"
            )
            
            endpoint = st.text_input(
                "Endpoint URL *",
                value=edit_config.get('endpoint', ''),
                placeholder="https://your-resource.openai.azure.com",
                help="Azure OpenAI 资源的 endpoint URL"
            )
            
            api_version = st.text_input(
                "API Version",
                value=edit_config.get('api_version', '2024-02-15-preview'),
                help="Azure OpenAI API 版本"
            )
        
        with col2:
            api_key = st.text_input(
                "API Key *",
                value=edit_config.get('api_key', ''),
                type="password",
                help="Azure OpenAI 资源的 API key"
            )
            
            description = st.text_area(
                "描述",
                value=edit_config.get('description', ''),
                placeholder="配置的用途描述...",
                help="可选的配置描述"
            )
        
        st.markdown("---")
        st.markdown("### 推理参数配置")
        
        # 检查是否支持推理
        supports_reasoning = model_name in REASONING_SUPPORTED_MODELS if model_name else False
        
        col3, col4 = st.columns(2)
        
        with col3:
            reasoning_enabled = st.checkbox(
                "启用推理模式",
                value=edit_config.get('reasoning_enabled', False),
                disabled=not supports_reasoning,
                help="仅 GPT-5 系列和 o 系列模型支持" if not supports_reasoning else REASONING_HELP
            )
        
        with col4:
            reasoning_effort = st.selectbox(
                "推理级别",
                options=list(REASONING_EFFORTS.keys()),
                format_func=lambda x: REASONING_EFFORTS[x],
                index=list(REASONING_EFFORTS.keys()).index(edit_config.get('reasoning_effort', 'low')),
                disabled=not reasoning_enabled or not supports_reasoning
            )
        
        if not supports_reasoning and model_name:
            st.warning(f"⚠️ 模型 `{model_name}` 不支持推理参数，推理配置将被忽略。")
        
        st.markdown("---")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn1:
            submit = st.form_submit_button("💾 保存配置", use_container_width=True)
        with col_btn2:
            test = st.form_submit_button("🧪 测试连接", use_container_width=True)
        with col_btn3:
            cancel = st.form_submit_button("❌ 取消", use_container_width=True)
        
        if cancel:
            st.session_state.show_add_form = False
            st.session_state.editing_config = None
            st.rerun()
        
        if submit or test:
            # 验证必填字段
            errors = []
            if not model_name:
                errors.append("模型名称不能为空")
            if not endpoint:
                errors.append("Endpoint URL 不能为空")
            elif not validate_endpoint(endpoint):
                errors.append("Endpoint URL 格式不正确")
            if not api_key:
                errors.append("API Key 不能为空")
            elif not validate_api_key(api_key):
                errors.append("API Key 格式不正确（至少32个字符）")
            
            if errors:
                st.error("❌ 验证失败:\n- " + "\n- ".join(errors))
            else:
                new_config = {
                    'model_name': model_name,
                    'endpoint': endpoint,
                    'api_key': api_key,
                    'api_version': api_version,
                    'reasoning_enabled': reasoning_enabled and supports_reasoning,
                    'reasoning_effort': reasoning_effort if reasoning_enabled and supports_reasoning else 'none',
                    'description': description,
                    'created_at': edit_config.get('created_at', datetime.now().isoformat()),
                    'updated_at': datetime.now().isoformat()
                }
                
                if test:
                    # 测试连接
                    with st.spinner("🔄 正在测试连接..."):
                        success, message = test_config(new_config)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                
                if submit:
                    # 保存配置
                    if st.session_state.editing_config is not None:
                        # 更新现有配置
                        new_config['id'] = st.session_state.editing_config['id']
                        for i, conf in enumerate(configs):
                            if conf['id'] == new_config['id']:
                                configs[i] = new_config
                                break
                    else:
                        # 添加新配置
                        new_config['id'] = get_unique_config_id(configs)
                        configs.append(new_config)
                    
                    if save_configs(configs):
                        st.success("✅ 配置保存成功！")
                        st.session_state.show_add_form = False
                        st.session_state.editing_config = None
                        st.rerun()

else:
    # 显示配置列表
    st.subheader("📋 已保存的配置")
    
    if not configs:
        st.info("📝 还没有任何配置。点击左侧的 **➕ 添加新配置** 按钮开始添加。")
    else:
        # 搜索和过滤
        col_search, col_filter = st.columns([3, 1])
        with col_search:
            search_term = st.text_input("🔍 搜索配置", placeholder="输入模型名称或描述...")
        with col_filter:
            filter_reasoning = st.selectbox(
                "过滤推理模式",
                options=["全部", "已启用", "未启用"]
            )
        
        # 过滤配置
        filtered_configs = configs
        if search_term:
            filtered_configs = [
                c for c in filtered_configs
                if search_term.lower() in c['model_name'].lower() or
                   search_term.lower() in c.get('description', '').lower()
            ]
        if filter_reasoning == "已启用":
            filtered_configs = [c for c in filtered_configs if c.get('reasoning_enabled', False)]
        elif filter_reasoning == "未启用":
            filtered_configs = [c for c in filtered_configs if not c.get('reasoning_enabled', False)]
        
        st.markdown(f"**显示 {len(filtered_configs)} / {len(configs)} 个配置**")
        st.markdown("---")
        
        # 显示配置卡片
        for config in filtered_configs:
            with st.container():
                st.markdown('<div class="config-card">', unsafe_allow_html=True)
                
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                
                with col1:
                    st.markdown(f'<div class="config-header">🤖 {config["model_name"]}</div>', unsafe_allow_html=True)
                    if config.get('description'):
                        st.caption(config['description'])
                
                with col2:
                    if st.button("🧪 测试", key=f"test_{config['id']}", use_container_width=True):
                        with st.spinner("测试中..."):
                            success, message = test_config(config)
                            if success:
                                st.success(message, icon="✅")
                            else:
                                st.error(message, icon="❌")
                
                with col3:
                    if st.button("✏️ 编辑", key=f"edit_{config['id']}", use_container_width=True):
                        st.session_state.editing_config = config
                        st.session_state.show_add_form = False
                        st.rerun()
                
                with col4:
                    if st.button("📋 复制", key=f"copy_{config['id']}", use_container_width=True):
                        new_config = config.copy()
                        new_config['id'] = get_unique_config_id(configs)
                        new_config['model_name'] = f"{config['model_name']}-copy"
                        new_config['created_at'] = datetime.now().isoformat()
                        new_config['updated_at'] = datetime.now().isoformat()
                        configs.append(new_config)
                        if save_configs(configs):
                            st.success("✅ 配置已复制！")
                            st.rerun()
                
                with col5:
                    if st.button("🗑️ 删除", key=f"delete_{config['id']}", use_container_width=True):
                        if st.session_state.get(f"confirm_delete_{config['id']}", False):
                            configs = [c for c in configs if c['id'] != config['id']]
                            if save_configs(configs):
                                st.success("✅ 配置已删除！")
                                st.session_state[f"confirm_delete_{config['id']}"] = False
                                st.rerun()
                        else:
                            st.session_state[f"confirm_delete_{config['id']}"] = True
                            st.warning("⚠️ 再次点击确认删除")
                
                # 显示配置详情
                with st.expander("📖 查看配置详情"):
                    st.markdown(f'<div class="config-field"><strong>Endpoint:</strong> {config["endpoint"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="config-field"><strong>API Version:</strong> {config.get("api_version", "N/A")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="config-field"><strong>API Key:</strong> {"*" * 40}</div>', unsafe_allow_html=True)
                    
                    if config.get('reasoning_enabled', False):
                        st.markdown(
                            f'<div class="config-field"><strong>推理模式:</strong> ✅ 已启用 '
                            f'({REASONING_EFFORTS[config.get("reasoning_effort", "low")]})</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown('<div class="config-field"><strong>推理模式:</strong> ❌ 未启用</div>', unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="config-field"><strong>创建时间:</strong> {config.get("created_at", "N/A")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="config-field"><strong>更新时间:</strong> {config.get("updated_at", "N/A")}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

# 页面底部帮助信息
with st.expander("❓ 使用帮助"):
    st.markdown("""
    ### 如何使用模型配置管理
    
    1. **添加新配置**
       - 点击左侧的 **➕ 添加新配置** 按钮
       - 填写必填字段：模型名称、Endpoint URL、API Key
       - 如果模型支持推理（GPT-5 系列、o 系列），可以启用推理模式并选择推理级别
       - 点击 **🧪 测试连接** 验证配置是否正确
       - 点击 **💾 保存配置** 保存
    
    2. **管理现有配置**
       - **测试**: 验证配置是否可用
       - **编辑**: 修改配置信息
       - **复制**: 快速创建相似配置
       - **删除**: 移除不需要的配置（需要二次确认）
    
    3. **导入/导出**
       - 使用 **📥 导出配置文件** 备份您的配置
       - 使用 **📤 导入配置文件** 从备份恢复或迁移配置
    
    4. **推理参数说明**
       - 仅 GPT-5 系列和 o 系列模型支持推理参数
       - 推理级别越高，模型会花费更多时间思考，响应质量可能更好
       - 根据任务复杂度选择合适的推理级别
    
    ### 配置文件位置
    
    配置保存在: `model_configs.json`
    
    ### 安全提示
    
    ⚠️ **注意**: API Key 以明文形式保存在配置文件中。请确保:
    - 不要将配置文件提交到公共代码仓库
    - 适当设置文件访问权限
    - 定期更换 API Key
    - 在生产环境中使用 Azure Key Vault 等密钥管理服务
    """)
