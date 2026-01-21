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
        "Endpoint",
        value=realtime_config.get('endpoint', ''),
        placeholder="https://your-resource.openai.azure.com",
        help="不需要包含 /realtime 路径",
        key="realtime_endpoint"
    )
    
    deployment = st.text_input(
        "Deployment Name",
        value=realtime_config.get('deployment', 'gpt-4o-realtime-preview'),
        help="Realtime 模型部署名称",
        key="realtime_deployment"
    )
    
    # 保存配置按钮
    if st.button("💾 保存 Realtime 配置", use_container_width=True):
        config['realtime'] = {
            'api_key': api_key,
            'endpoint': endpoint,
            'deployment': deployment
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
    st.warning("⚠️ 请先在侧边栏配置 API Key、Endpoint 和 Deployment Name，并保存配置")
else:
    # 构建 Realtime Endpoint
    realtime_endpoint = f"{endpoint}/openai/realtime"
    
    st.success("✅ 配置已完成，准备开始对话")
    
    # 显示配置信息
    with st.expander("📋 当前配置"):
        st.code(f"""
Endpoint: {realtime_endpoint}
Deployment: {deployment}
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
            .stop-btn {{
                background-color: #f44336;
                color: white;
            }}
            .stop-btn:hover {{
                background-color: #da190b;
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
        </div>
        
        <script>
            const API_KEY = "{api_key}";
            const ENDPOINT = "{realtime_endpoint}";
            const DEPLOYMENT = "{deployment}";
            
            let peerConnection = null;
            let dataChannel = null;
            
            function updateStatus(message, type = 'idle') {{
                const statusEl = document.getElementById('status');
                statusEl.textContent = message;
                statusEl.className = 'status ' + type;
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
                    
                    // 创建 RTCPeerConnection
                    peerConnection = new RTCPeerConnection();
                    
                    // 添加音频轨道
                    const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                    stream.getTracks().forEach(track => {{
                        peerConnection.addTrack(track, stream);
                    }});
                    
                    // 创建 Data Channel
                    dataChannel = peerConnection.createDataChannel('oai-events');
                    
                    dataChannel.onopen = () => {{
                        updateStatus('✅ 已连接，可以开始说话了！', 'connected');
                        document.getElementById('stopBtn').disabled = false;
                    }};
                    
                    dataChannel.onmessage = (event) => {{
                        try {{
                            const message = JSON.parse(event.data);
                            console.log('Received:', message);
                            
                            if (message.type === 'response.audio_transcript.done') {{
                                addMessage(message.transcript, 'assistant');
                            }} else if (message.type === 'conversation.item.input_audio_transcription.completed') {{
                                addMessage(message.transcript, 'user');
                            }}
                        }} catch (error) {{
                            console.error('Error parsing message:', error);
                        }}
                    }};
                    
                    dataChannel.onerror = (error) => {{
                        updateStatus('❌ 连接错误: ' + error, 'error');
                    }};
                    
                    // 创建 Offer
                    const offer = await peerConnection.createOffer();
                    await peerConnection.setLocalDescription(offer);
                    
                    // 发送 Offer 到 Azure
                    const url = `${{ENDPOINT}}?deployment=${{DEPLOYMENT}}&api-version=2024-10-01-preview`;
                    
                    const response = await fetch(url, {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/sdp',
                            'api-key': API_KEY
                        }},
                        body: offer.sdp
                    }});
                    
                    if (!response.ok) {{
                        throw new Error('Failed to connect: ' + response.statusText);
                    }}
                    
                    const answerSdp = await response.text();
                    await peerConnection.setRemoteDescription({{
                        type: 'answer',
                        sdp: answerSdp
                    }});
                    
                }} catch (error) {{
                    console.error('Error:', error);
                    updateStatus('❌ 连接失败: ' + error.message, 'error');
                    document.getElementById('startBtn').disabled = false;
                }}
            }}
            
            function stopSession() {{
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
        </script>
    </body>
    </html>
    """
    
    # 显示 WebRTC 界面
    html(webrtc_html, height=700, scrolling=True)
    
    # 技术说明
    st.markdown("---")
    
    with st.expander("🔧 技术说明"):
        st.markdown("""
        ### WebRTC 流程
        
        1. **创建 RTCPeerConnection**
           - 建立 WebRTC 连接
        
        2. **获取麦克风权限**
           - `navigator.mediaDevices.getUserMedia()`
        
        3. **创建 Data Channel**
           - 用于接收转录文本和事件
        
        4. **发送 SDP Offer**
           - POST 到 `/openai/realtime` 端点
        
        5. **接收 SDP Answer**
           - 设置远程描述完成连接
        
        6. **实时通信**
           - 音频流：通过 WebRTC 传输
           - 文本转录：通过 Data Channel 接收
        
        ### API 端点格式
        ```
        POST {endpoint}/openai/realtime?deployment={deployment}&api-version=2024-10-01-preview
        Headers:
          Content-Type: application/sdp
          api-key: {your-api-key}
        Body: SDP Offer
        ```
        
        ### 支持的事件
        - `response.audio_transcript.done` - GPT 回复的转录
        - `conversation.item.input_audio_transcription.completed` - 用户输入的转录
        
        ### 参考文档
        [Azure OpenAI Realtime Audio](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/realtime-audio-webrtc)
        """)
