"""
GPT Realtime Audio 测试
使用 WebRTC 进行实时语音对话
"""

import streamlit as st
from streamlit.components.v1 import html
import json
from pathlib import Path

# 页面配置
st.set_page_config(
    page_title="GPT Realtime Audio",
    page_icon="🎤",
    layout="wide"
)

# 加载配置
CONFIG_FILE = Path("config.json")

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

config = load_config()

# 标题
st.title("🎤 GPT Realtime Audio 测试")
st.markdown("使用 WebRTC 与 GPT 进行实时语音对话")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ Realtime 模型配置")
    
    # 从配置文件加载 realtime 模型的配置
    realtime_config = config.get('realtime', {})
    
    api_key = st.text_input(
        "API Key",
        type="password",
        value=realtime_config.get('api_key', ''),
        help="Azure OpenAI API Key",
        key="realtime_api_key"
    )
    
    endpoint = st.text_input(
        "完整 Endpoint URL",
        value=realtime_config.get('endpoint', ''),
        placeholder="https://xxx.cognitiveservices.azure.com/openai/realtime",
        help="完整的 realtime 端点 URL（包含 /openai/realtime）",
        key="realtime_endpoint"
    )
    
    deployment = st.text_input(
        "Deployment Name",
        value=realtime_config.get('deployment', 'gpt-realtime'),
        help="Realtime 模型部署名称",
        key="realtime_deployment"
    )
    
    api_version = st.text_input(
        "API Version",
        value=realtime_config.get('api_version', '2024-10-01-preview'),
        help="Azure OpenAI API 版本",
        key="realtime_api_version"
    )
    
    # 保存配置按钮
    if st.button("💾 保存 Realtime 配置", use_container_width=True):
        config['realtime'] = {
            'api_key': api_key,
            'endpoint': endpoint,
            'deployment': deployment,
            'api_version': api_version
        }
        if save_config(config):
            st.success("✅ Realtime 配置已保存！")
        else:
            st.error("❌ 保存失败")
    
    st.divider()
    
    st.subheader("📖 使用说明")
    st.markdown("""
    1. 输入配置信息
    2. 点击 "💾 保存 Realtime 配置"
    3. 点击 "🎤 开始对话" 按钮
    4. 允许浏览器使用麦克风
    5. 开始说话，GPT 会实时回复
    6. 点击 "🛑 停止对话" 结束
    """)
    
    st.divider()
    
    st.info("⚠️ 需要浏览器支持 WebRTC 和麦克风权限")

# 主界面
if not api_key or not endpoint or not deployment:
    st.warning("⚠️ 请先在侧边栏配置 API Key、Endpoint、Deployment Name 和 API Version，并保存配置")
else:
    st.success("✅ 配置已完成，准备开始对话")
    
    # 显示配置信息
    with st.expander("📋 当前配置"):
        st.code(f"""
Endpoint: {endpoint}
Deployment: {deployment}
API Version: {api_version}
API Key: {"*" * 40}
        """)
    
    # WebRTC 音频界面
    st.markdown("---")
    
    # 创建 HTML/JavaScript 代码用于 WebRTC
    webrtc_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .button {{
                padding: 15px 30px;
                font-size: 18px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin: 10px;
                transition: all 0.3s;
            }}
            .start-btn {{
                background-color: #4CAF50;
                color: white;
            }}
            .start-btn:hover {{
                background-color: #45a049;
            }}
            .start-btn:disabled {{
                background-color: #cccccc;
                cursor: not-allowed;
            }}
            .stop-btn {{
                background-color: #f44336;
                color: white;
            }}
            .stop-btn:hover {{
                background-color: #da190b;
            }}
            .stop-btn:disabled {{
                background-color: #cccccc;
                cursor: not-allowed;
            }}
            .status {{
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
                font-size: 16px;
            }}
            .status.idle {{
                background-color: #e3f2fd;
                color: #1976d2;
            }}
            .status.connecting {{
                background-color: #fff3e0;
                color: #f57c00;
            }}
            .status.connected {{
                background-color: #e8f5e9;
                color: #388e3c;
            }}
            .status.error {{
                background-color: #ffebee;
                color: #c62828;
            }}
            .transcript {{
                margin-top: 20px;
                padding: 15px;
                background-color: #f9f9f9;
                border-radius: 5px;
                min-height: 200px;
                max-height: 400px;
                overflow-y: auto;
            }}
            .message {{
                margin: 10px 0;
                padding: 10px;
                border-radius: 5px;
            }}
            .user-message {{
                background-color: #e3f2fd;
                text-align: right;
            }}
            .assistant-message {{
                background-color: #f1f8e9;
                text-align: left;
            }}
            .debug {{
                margin-top: 20px;
                padding: 10px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 12px;
                max-height: 200px;
                overflow-y: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🎤 实时语音对话</h2>
            
            <div class="status idle" id="status">
                准备就绪
            </div>
            
            <div>
                <button class="button start-btn" id="startBtn" onclick="startSession()">
                    🎤 开始对话
                </button>
                <button class="button stop-btn" id="stopBtn" onclick="stopSession()" disabled>
                    🛑 停止对话
                </button>
            </div>
            
            <div class="transcript" id="transcript">
                <p style="color: #999;">对话内容将显示在这里...</p>
            </div>
            
            <div class="debug" id="debug">
                <strong>调试信息:</strong><br>
            </div>
        </div>
        
        <script>
            const API_KEY = "{api_key}";
            const ENDPOINT = "{endpoint}";
            const DEPLOYMENT = "{deployment}";
            const API_VERSION = "{api_version}";
            
            let peerConnection = null;
            let dataChannel = null;
            
            function addDebug(message) {{
                const debugEl = document.getElementById('debug');
                const time = new Date().toLocaleTimeString();
                debugEl.innerHTML += `[${{time}}] ${{message}}<br>`;
                debugEl.scrollTop = debugEl.scrollHeight;
                console.log(message);
            }}
            
            function updateStatus(message, type = 'idle') {{
                const statusEl = document.getElementById('status');
                statusEl.textContent = message;
                statusEl.className = 'status ' + type;
                addDebug('Status: ' + message);
            }}
            
            function addMessage(content, role) {{
                const transcript = document.getElementById('transcript');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message ' + role + '-message';
                messageDiv.textContent = content;
                transcript.appendChild(messageDiv);
                transcript.scrollTop = transcript.scrollHeight;
            }}
            
            async function startSession() {{
                try {{
                    updateStatus('正在连接...', 'connecting');
                    document.getElementById('startBtn').disabled = true;
                    
                    addDebug('开始创建 RTCPeerConnection...');
                    
                    // 创建 RTCPeerConnection
                    peerConnection = new RTCPeerConnection();
                    
                    addDebug('请求麦克风权限...');
                    
                    // 添加音频轨道
                    const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                    addDebug('麦克风权限已获取');
                    
                    stream.getTracks().forEach(track => {{
                        peerConnection.addTrack(track, stream);
                        addDebug('添加音频轨道: ' + track.label);
                    }});
                    
                    // 创建 Data Channel
                    addDebug('创建 Data Channel...');
                    dataChannel = peerConnection.createDataChannel('oai-events');
                    
                    dataChannel.onopen = () => {{
                        updateStatus('✅ 已连接，可以开始说话了！', 'connected');
                        document.getElementById('stopBtn').disabled = false;
                        addDebug('Data Channel 已打开');
                    }};
                    
                    dataChannel.onmessage = (event) => {{
                        try {{
                            const message = JSON.parse(event.data);
                            addDebug('收到消息: ' + message.type);
                            
                            if (message.type === 'response.audio_transcript.done') {{
                                addMessage(message.transcript, 'assistant');
                            }} else if (message.type === 'conversation.item.input_audio_transcription.completed') {{
                                addMessage(message.transcript, 'user');
                            }}
                        }} catch (error) {{
                            addDebug('解析消息错误: ' + error.message);
                        }}
                    }};
                    
                    dataChannel.onerror = (error) => {{
                        updateStatus('❌ Data Channel 错误', 'error');
                        addDebug('Data Channel 错误: ' + error);
                    }};
                    
                    // 创建 Offer
                    addDebug('创建 SDP Offer...');
                    const offer = await peerConnection.createOffer();
                    await peerConnection.setLocalDescription(offer);
                    addDebug('SDP Offer 已创建');
                    
                    // 构建完整 URL（endpoint 已经包含 /openai/realtime）
                    const url = `${{ENDPOINT}}?api-version=${{API_VERSION}}&deployment=${{DEPLOYMENT}}`;
                    addDebug('请求 URL: ' + url);
                    
                    // 发送 Offer 到 Azure
                    addDebug('发送 SDP Offer 到 Azure...');
                    const response = await fetch(url, {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/sdp',
                            'api-key': API_KEY
                        }},
                        body: offer.sdp
                    }});
                    
                    addDebug('响应状态: ' + response.status + ' ' + response.statusText);
                    
                    if (!response.ok) {{
                        const errorText = await response.text();
                        addDebug('错误响应: ' + errorText);
                        throw new Error('Failed to connect: ' + response.statusText + ' - ' + errorText);
                    }}
                    
                    const answerSdp = await response.text();
                    addDebug('收到 SDP Answer，长度: ' + answerSdp.length);
                    
                    await peerConnection.setRemoteDescription({{
                        type: 'answer',
                        sdp: answerSdp
                    }});
                    
                    addDebug('连接建立成功！');
                    
                }} catch (error) {{
                    console.error('Error:', error);
                    updateStatus('❌ 连接失败: ' + error.message, 'error');
                    addDebug('连接失败: ' + error.message);
                    document.getElementById('startBtn').disabled = false;
                }}
            }}
            
            function stopSession() {{
                addDebug('断开连接...');
                
                if (peerConnection) {{
                    peerConnection.close();
                    peerConnection = null;
                }}
                if (dataChannel) {{
                    dataChannel.close();
                    dataChannel = null;
                }}
                
                updateStatus('已断开连接', 'idle');
                document.getElementById('startBtn').disabled = false;
                document.getElementById('stopBtn').disabled = true;
            }}
            
            // 初始化调试信息
            addDebug('页面已加载');
            addDebug('Endpoint: ' + ENDPOINT);
            addDebug('Deployment: ' + DEPLOYMENT);
            addDebug('API Version: ' + API_VERSION);
            addDebug('API Version: ' + API_VERSION);
        </script>
    </body>
    </html>
    """
    
    # 显示 WebRTC 界面
    html(webrtc_html, height=900, scrolling=True)
    
    # 技术说明
    st.markdown("---")
    
    with st.expander("🔧 配置说明"):
        st.markdown(f"""
        ### Endpoint 格式
        
        你的配置：
        ```
        {endpoint}
        ```
        
        正确的格式应该是：
        ```
        https://your-resource.cognitiveservices.azure.com/openai/realtime
        ```
        
        完整的请求 URL 将是：
        ```
        {endpoint}?api-version={api_version}&deployment={deployment}
        ```
        
        ### 常见问题
        
        1. **Endpoint 不需要包含查询参数**
           - ❌ 错误：包含 `?api-version=...`
           - ✅ 正确：只到 `/openai/realtime`
        
        2. **Deployment 是部署名称**
           - 在 Azure Portal 中创建的部署名称
           - 通常是 `gpt-realtime` 或 `gpt-4o-realtime-preview`
        
        3. **API Key 权限**
           - 需要有访问 Realtime API 的权限
           - 在 Azure Portal 的 Keys and Endpoint 中获取
        """)
