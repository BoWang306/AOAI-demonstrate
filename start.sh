#!/bin/bash

# Azure OpenAI 模型测试门户启动脚本

echo "🚀 启动 Azure OpenAI 模型测试门户..."
echo ""

# 检查依赖
if ! command -v streamlit &> /dev/null; then
    echo "📦 安装依赖..."
    pip install -q -r requirements.txt
fi

# 检查环境变量文件
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件"
    echo "💡 提示: 复制 .env.example 并填入你的配置"
    echo ""
fi

# 启动应用
echo "✅ 启动应用..."
echo ""
echo "📱 访问方式:"
echo "   本地: http://localhost:8501"
echo "   网络: http://0.0.0.0:8501"
echo ""
echo "⌨️  按 Ctrl+C 停止应用"
echo ""

streamlit run app.py --server.port 8501 --server.address 0.0.0.0
