"""
通用 UI 组件
"""

import streamlit as st


def display_error(error_dict: dict):
    """显示友好的错误信息"""
    st.error(f"❌ **{error_dict['title']}**")
    st.error(error_dict['description'])
    
    if 'solutions' in error_dict:
        st.info("💡 **解决方案**:")
        for solution in error_dict['solutions']:
            st.info(f"• {solution}")


def display_metrics(metrics: dict):
    """显示性能指标"""
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⏱️ 延迟", f"{metrics['latency']:.2f}s")
    col2.metric("📥 输入 Tokens", metrics['prompt_tokens'])
    col3.metric("📤 输出 Tokens", metrics['completion_tokens'])
    col4.metric("📊 总计 Tokens", metrics['total_tokens'])


def display_config_details(config: dict):
    """显示配置详情"""
    st.markdown(f'<div class="config-field"><strong>模型:</strong> {config["model_name"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="config-field"><strong>Endpoint:</strong> {config["endpoint"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="config-field"><strong>API Version:</strong> {config.get("api_version", "N/A")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="config-field"><strong>API Key:</strong> {"*" * 40}</div>', unsafe_allow_html=True)
    
    if config.get('reasoning_enabled', False):
        st.markdown(
            f'<div class="config-field"><strong>推理模式:</strong> ✅ 已启用 ({config.get("reasoning_effort", "low")})</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown('<div class="config-field"><strong>推理模式:</strong> ❌ 未启用</div>', unsafe_allow_html=True)
    
    if config.get('description'):
        st.markdown(f'<div class="config-field"><strong>描述:</strong> {config["description"]}</div>', unsafe_allow_html=True)
