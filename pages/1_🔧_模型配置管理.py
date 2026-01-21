"""
模型配置管理页面
"""

import streamlit as st
import json
from datetime import datetime
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config_manager import ConfigManager
from lib.api_client import AzureOpenAIClient
from lib.models import REASONING_EFFORTS, REASONING_SUPPORTED_MODELS, REASONING_HELP
from utils.styles import CUSTOM_CSS
from utils.ui_components import display_config_details

# 页面配置
st.set_page_config(
    page_title="模型配置管理",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用样式
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 初始化配置管理器
config_manager = ConfigManager()

# 初始化 session state
if 'editing_config' not in st.session_state:
    st.session_state.editing_config = None
if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False

def test_config(config: dict) -> tuple[bool, str]:
    """测试配置"""
    try:
        client = AzureOpenAIClient(
            config['api_key'],
            config['endpoint'],
            config.get('api_version', '2024-02-15-preview')
        )
        
        reasoning_effort = None
        if config.get('reasoning_enabled', False):
            reasoning_effort = config.get('reasoning_effort', 'low')
        
        return client.test_connection(config['model_name'], reasoning_effort)
    except Exception as e:
        return False, f"❌ 测试失败: {str(e)}"

def main():
    st.title("🔧 模型配置管理")
    st.markdown("管理多个 Azure OpenAI 模型的配置")
    
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
        
        configs = config_manager.load_configs()
        if configs:
            config_json = json.dumps(configs, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 导出配置文件",
                data=config_json,
                file_name=f"model_configs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        uploaded_file = st.file_uploader("📤 导入配置文件", type=['json'])
        if uploaded_file is not None:
            try:
                imported_configs = json.load(uploaded_file)
                if isinstance(imported_configs, list):
                    if st.button("确认导入", use_container_width=True):
                        if config_manager.save_configs(imported_configs):
                            st.success("✅ 配置导入成功！")
                            st.rerun()
                else:
                    st.error("❌ 配置文件格式错误！")
            except Exception as e:
                st.error(f"❌ 导入失败: {str(e)}")
        
        st.markdown("---")
        st.info(f"📊 当前配置数量: **{len(configs)}**")
    
    # 主内容
    configs = config_manager.load_configs()
    
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
                    placeholder="例如: gpt-5.2"
                )
                
                endpoint = st.text_input(
                    "Endpoint URL *",
                    value=edit_config.get('endpoint', ''),
                    placeholder="https://your-resource.openai.azure.com"
                )
                
                api_version = st.text_input(
                    "API Version",
                    value=edit_config.get('api_version', '2024-02-15-preview')
                )
            
            with col2:
                api_key = st.text_input(
                    "API Key *",
                    value=edit_config.get('api_key', ''),
                    type="password"
                )
                
                description = st.text_area(
                    "描述",
                    value=edit_config.get('description', ''),
                    placeholder="配置的用途描述..."
                )
            
            st.markdown("---")
            st.markdown("### 推理参数配置")
            
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
                st.warning(f"⚠️ 模型 `{model_name}` 不支持推理参数")
            
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
                # 验证
                errors = []
                if not model_name:
                    errors.append("模型名称不能为空")
                if not endpoint:
                    errors.append("Endpoint URL 不能为空")
                elif not config_manager.validate_endpoint(endpoint):
                    errors.append("Endpoint URL 格式不正确")
                if not api_key:
                    errors.append("API Key 不能为空")
                elif not config_manager.validate_api_key(api_key):
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
                        with st.spinner("🔄 正在测试连接..."):
                            success, message = test_config(new_config)
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
                    
                    if submit:
                        if st.session_state.editing_config is not None:
                            # 更新配置
                            configs = config_manager.update_config(
                                configs,
                                st.session_state.editing_config['id'],
                                new_config
                            )
                        else:
                            # 添加新配置
                            configs = config_manager.add_config(configs, new_config)
                        
                        if config_manager.save_configs(configs):
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
                            configs = config_manager.copy_config(configs, config['id'])
                            if config_manager.save_configs(configs):
                                st.success("✅ 配置已复制！")
                                st.rerun()
                    
                    with col5:
                        if st.button("🗑️ 删除", key=f"delete_{config['id']}", use_container_width=True):
                            if st.session_state.get(f"confirm_delete_{config['id']}", False):
                                configs = config_manager.delete_config(configs, config['id'])
                                if config_manager.save_configs(configs):
                                    st.success("✅ 配置已删除！")
                                    st.session_state[f"confirm_delete_{config['id']}"] = False
                                    st.rerun()
                            else:
                                st.session_state[f"confirm_delete_{config['id']}"] = True
                                st.warning("⚠️ 再次点击确认删除")
                    
                    # 显示配置详情
                    with st.expander("📖 查看配置详情"):
                        display_config_details(config)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
