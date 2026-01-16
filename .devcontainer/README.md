# Azure OpenAI 模型测试门户 - Dev Container

这个 Dev Container 配置为 Azure OpenAI 模型测试门户提供了完整的开发环境。

## 🎯 功能特性

### 预安装工具
- ✅ Python 3.11
- ✅ Git
- ✅ GitHub CLI
- ✅ pip 和所有项目依赖

### VS Code 扩展
- Python 开发工具（Pylance、调试器）
- Black 代码格式化
- Jupyter Notebook 支持
- GitLens
- GitHub Copilot（如果已订阅）
- 拼写检查

### 自动配置
- 代码保存时自动格式化
- Python 代码检查（Flake8）
- 导入语句自动整理
- 端口 8501 自动转发（Streamlit）

## 🚀 快速开始

### 方法 1: VS Code (推荐)

1. **安装 VS Code 和扩展**
   - 安装 [Visual Studio Code](https://code.visualstudio.com/)
   - 安装 [Dev Containers 扩展](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. **打开项目**
   ```bash
   code /path/to/webapp
   ```

3. **启动 Dev Container**
   - VS Code 会提示 "Reopen in Container"
   - 或者按 `F1`，输入 "Dev Containers: Reopen in Container"
   - 等待容器构建和依赖安装

4. **开始开发**
   ```bash
   # 在容器内的终端运行
   streamlit run app.py
   ```

### 方法 2: GitHub Codespaces

1. **创建 Codespace**
   - 在 GitHub 仓库页面点击 "Code" → "Codespaces" → "Create codespace"
   - 等待环境准备完成

2. **启动应用**
   ```bash
   streamlit run app.py
   ```

3. **访问应用**
   - Codespaces 会自动转发端口 8501
   - 点击弹出的通知访问应用

## 🏗️ 配置说明

### Dockerfile

- **位置**: `.devcontainer/Dockerfile`
- **基础镜像**: `mcr.microsoft.com/devcontainers/python:3.11`
- **特性**: 
  - 预安装系统工具
  - 预安装 Python 依赖
  - 健康检查配置
  - 适用于开发和生产

### devcontainer.json

- **位置**: `.devcontainer/devcontainer.json`
- **配置内容**:
  - Dockerfile 构建配置
  - VS Code 扩展和设置
  - 端口转发
  - 挂载点配置

## ⚙️ 高级配置

### 环境变量

在容器中配置 Azure OpenAI API：

**方法 1: 使用 .env 文件（推荐）**
```bash
# 在容器内创建 .env 文件
cp .env.example .env
nano .env
```

**方法 2: 在 devcontainer.json 中配置**
```json
"remoteEnv": {
  "AZURE_OPENAI_API_KEY": "${localEnv:AZURE_OPENAI_API_KEY}",
  "AZURE_OPENAI_ENDPOINT": "${localEnv:AZURE_OPENAI_ENDPOINT}"
}
```

### Azure CLI 凭证

Dev Container 会自动挂载你的本地 Azure CLI 配置：
```
~/.azure → /home/vscode/.azure
```

这样你可以在容器内直接使用本地的 Azure 认证。

## 🔧 自定义配置

### 添加更多 VS Code 扩展

编辑 `.devcontainer/devcontainer.json`：
```json
"customizations": {
  "vscode": {
    "extensions": [
      "现有扩展...",
      "你的扩展ID"
    ]
  }
}
```

### 修改 Python 版本

在 `.devcontainer/Dockerfile` 中更改 ARG：
```dockerfile
ARG VARIANT="3.10"  # 或 3.9, 3.11, 3.12
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}
```

### 安装额外的系统包

在 `.devcontainer/Dockerfile` 中添加：
```dockerfile
RUN apt-get update && apt-get install -y \
    你的包名 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

## 📚 使用技巧

### 1. 在容器中运行应用

```bash
# 启动主应用
streamlit run app.py

# 启动配置助手
streamlit run config_helper.py

# 使用启动脚本
./start.sh
```

### 2. Python 开发

```bash
# 安装新依赖
pip install 包名

# 更新 requirements.txt
pip freeze > requirements.txt

# 运行 Python 脚本
python your_script.py
```

### 3. Git 操作

```bash
# Git 已预安装
git status
git add .
git commit -m "your message"
git push
```

### 4. 调试

- 在代码中设置断点（点击行号左侧）
- 按 `F5` 开始调试
- 或者在 VS Code 中选择 "Run and Debug"

### 5. Jupyter Notebook

```bash
# 容器已安装 Jupyter 支持
# 直接在 VS Code 中创建和运行 .ipynb 文件
```

## 🐛 故障排查

### 问题 1: 容器构建失败

**解决方案**:
```bash
# 重建容器
F1 → Dev Containers: Rebuild Container

# 或清理并重建
F1 → Dev Containers: Rebuild Container Without Cache
```

### 问题 2: 端口转发不工作

**解决方案**:
1. 检查防火墙设置
2. 手动转发端口：
   ```bash
   F1 → Forward a Port → 输入 8501
   ```

### 问题 3: Python 依赖安装失败

**解决方案**:
```bash
# 在容器终端中手动安装
pip install --upgrade pip
pip install -r requirements.txt
```

### 问题 4: 容器名称冲突

**错误信息**: `The container name "/azure-openai-portal-dev" is already in use`

**解决方案**:
```bash
# 删除现有容器
docker rm -f azure-openai-portal-dev

# 或在 devcontainer.json 中更改容器名称
"runArgs": ["--name", "azure-openai-portal-dev-2"]
```

## 🐳 Docker 相关

### 查看容器信息

```bash
# 查看运行的容器
docker ps

# 查看容器日志
docker logs azure-openai-portal-dev

# 进入容器
docker exec -it azure-openai-portal-dev bash
```

### 构建生产镜像

参见根目录的 `DOCKER_REGISTRY.md` 文档：

```bash
# 使用自动化脚本
./build-and-push.sh v1.1.0

# 推送到容器注册表
./build-and-push.sh v1.1.0 myregistry.azurecr.io
```

## 🔐 安全最佳实践

### 保护敏感信息

1. ✅ 使用环境变量存储 API Key
2. ✅ 不要将 `.env` 文件提交到版本控制
3. ✅ 定期轮换 API Key
4. ✅ 使用专用的开发环境密钥

### 输入验证

1. ✅ 过滤敏感信息
2. ✅ 限制输入长度
3. ✅ 验证输入格式

## 📖 相关文档

- [VS Code Dev Containers 文档](https://code.visualstudio.com/docs/devcontainers/containers)
- [GitHub Codespaces 文档](https://docs.github.com/codespaces)
- [Dev Container 规范](https://containers.dev/)
- [Docker 镜像构建指南](../DOCKER_REGISTRY.md)

## 💡 开发工作流

### 典型工作流程

1. **打开项目**
   ```bash
   code /path/to/webapp
   # VS Code 提示 "Reopen in Container"
   ```

2. **等待容器启动**
   - 首次启动需要构建镜像（约 2-5 分钟）
   - 后续启动很快（约 10-30 秒）

3. **配置 API**
   ```bash
   cp .env.example .env
   # 编辑 .env 填入你的配置
   ```

4. **开发和测试**
   ```bash
   # 启动应用
   streamlit run app.py
   
   # 修改代码
   # Streamlit 会自动检测更改并提示重新运行
   ```

5. **提交代码**
   ```bash
   git add .
   git commit -m "your changes"
   git push
   ```

### 团队协作

**优势**:
- ✅ 统一的开发环境
- ✅ 自动安装依赖
- ✅ 配置即代码
- ✅ 新成员快速上手

**最佳实践**:
1. 将 `.devcontainer/` 提交到仓库
2. 文档化特定的配置需求
3. 使用 `.env.example` 说明需要的环境变量

## 🎉 完成！

现在你有了一个完整的 Dev Container 环境，可以：
- 🚀 快速启动开发
- 🔧 统一团队环境
- 📦 自动化配置
- 🌐 随处开发（本地、云端）
- 🐳 易于打包和部署

**祝开发愉快！**
