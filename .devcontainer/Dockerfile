FROM mcr.microsoft.com/devcontainers/python:3.11

# 设置工作目录
WORKDIR /workspace

# 安装额外的系统依赖（如果需要）
RUN apt-get update && apt-get install -y \
    vim \
    nano \
    curl \
    wget \
    tree \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip
RUN pip install --upgrade pip

# 复制 requirements.txt（在构建阶段安装依赖）
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 设置 Python 环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 设置默认命令（可被 docker run 覆盖）
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
