# Azure OpenAI 模型测试门户 - Dev Container Dockerfile
# 支持开发和生产部署

ARG VARIANT="3.11"
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}

# 设置工作目录
WORKDIR /workspace

# 安装系统依赖
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    vim \
    nano \
    curl \
    wget \
    tree \
    git \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip
RUN pip install --no-cache-dir --upgrade pip

# 设置 Python 环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 复制 requirements.txt (用于 Docker 镜像构建)
# Dev Container 会在 postCreateCommand 中重新安装
COPY requirements.txt /tmp/

# 预安装依赖（加速 Dev Container 启动）
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# 默认命令（可被覆盖）
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
