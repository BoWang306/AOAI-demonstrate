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

## ⚙️ 配置说明

### 端口转发

Dev Container 自动转发以下端口：
- **8501**: Streamlit 应用主端口

访问方式：
- VS Code: 点击终端中的 URL
- Codespaces: 自动弹出通知

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

### 安装额外的系统包

创建 `.devcontainer/Dockerfile`：
```dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.11

# 安装额外的系统包
RUN apt-get update && apt-get install -y \
    你的包名 \
    && apt-get clean
```

然后修改 `devcontainer.json`：
```json
"build": {
  "dockerfile": "Dockerfile"
}
```

### 修改 Python 版本

在 `devcontainer.json` 中更改基础镜像：
```json
"image": "mcr.microsoft.com/devcontainers/python:3.10"
```

支持的版本：3.8, 3.9, 3.10, 3.11, 3.12

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

### 问题 4: 环境变量未加载

**解决方案**:
```bash
# 检查 .env 文件是否存在
ls -la .env

# 手动加载
source .env

# 或在 Python 中验证
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('AZURE_OPENAI_API_KEY'))"
```

## 🔐 安全最佳实践

1. **不要提交 .env 文件**
   - 已在 .gitignore 中配置
   - 使用 .env.example 作为模板

2. **使用环境变量**
   - 避免在代码中硬编码敏感信息
   - 使用 VS Code 的 Secret Storage

3. **定期更新容器**
   ```bash
   F1 → Dev Containers: Rebuild Container
   ```

## 📖 相关文档

- [VS Code Dev Containers 文档](https://code.visualstudio.com/docs/devcontainers/containers)
- [GitHub Codespaces 文档](https://docs.github.com/codespaces)
- [Dev Container 规范](https://containers.dev/)

## 💡 开发工作流

### 典型工作流程

1. **打开项目**
   ```bash
   code /path/to/webapp
   # VS Code 提示 "Reopen in Container"
   ```

2. **等待容器启动**
   - 首次启动需要下载镜像和安装依赖（约 2-5 分钟）
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

**祝开发愉快！**
