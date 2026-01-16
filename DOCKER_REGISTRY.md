# Docker 镜像构建和推送指南

## 📦 概述

本项目提供了简化的 Docker 配置，易于构建、测试和推送到容器注册表。

## 🏗️ 项目结构

```
webapp/
├── .devcontainer/
│   ├── Dockerfile           # 主 Dockerfile（开发+生产）
│   ├── devcontainer.json    # VS Code Dev Container 配置
│   └── README.md            # Dev Container 说明
├── docker-compose.yml       # Docker Compose 配置（本地测试）
├── build-and-push.sh        # 构建和推送脚本
└── ...
```

## 🚀 快速开始

### 方法 1: 使用自动化脚本（推荐）

#### 本地构建

```bash
# 构建最新版本
./build-and-push.sh

# 构建指定版本
./build-and-push.sh v1.1.0
```

#### 推送到容器注册表

```bash
# 推送到 Docker Hub
./build-and-push.sh v1.1.0 yourusername

# 推送到 Azure Container Registry
./build-and-push.sh v1.1.0 yourregistry.azurecr.io

# 推送到 GitHub Container Registry
./build-and-push.sh v1.1.0 ghcr.io/yourusername
```

### 方法 2: 手动构建

#### 1. 构建镜像

```bash
# 基础构建
docker build -t azure-openai-portal:latest -f .devcontainer/Dockerfile .

# 带版本标签构建
docker build -t azure-openai-portal:v1.1.0 -f .devcontainer/Dockerfile .

# 构建并推送到注册表
docker build -t myregistry.azurecr.io/azure-openai-portal:v1.1.0 -f .devcontainer/Dockerfile .
```

#### 2. 测试镜像

```bash
# 运行容器
docker run -d -p 8501:8501 --name test-portal azure-openai-portal:latest

# 检查日志
docker logs test-portal

# 测试健康检查
docker exec test-portal curl -f http://localhost:8501/_stcore/health

# 停止并删除
docker stop test-portal && docker rm test-portal
```

#### 3. 推送到注册表

```bash
# 登录到容器注册表
docker login myregistry.azurecr.io

# 推送镜像
docker push myregistry.azurecr.io/azure-openai-portal:v1.1.0
docker push myregistry.azurecr.io/azure-openai-portal:latest
```

### 方法 3: 使用 Docker Compose

```bash
# 构建并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

## 🔧 容器注册表配置

### Docker Hub

```bash
# 1. 登录
docker login

# 2. 构建并推送
./build-and-push.sh v1.1.0 yourusername

# 3. 使用
docker pull yourusername/azure-openai-portal:v1.1.0
docker run -d -p 8501:8501 yourusername/azure-openai-portal:v1.1.0
```

### Azure Container Registry (ACR)

#### 创建 ACR

```bash
# 创建资源组
az group create --name myResourceGroup --location eastus

# 创建 ACR
az acr create --resource-group myResourceGroup \
  --name myregistry --sku Basic

# 登录
az acr login --name myregistry
```

#### 推送到 ACR

```bash
# 构建并推送
./build-and-push.sh v1.1.0 myregistry.azurecr.io

# 或手动
docker build -t myregistry.azurecr.io/azure-openai-portal:v1.1.0 -f .devcontainer/Dockerfile .
docker push myregistry.azurecr.io/azure-openai-portal:v1.1.0
```

#### 从 ACR 拉取

```bash
# 拉取
docker pull myregistry.azurecr.io/azure-openai-portal:v1.1.0

# 运行
docker run -d -p 8501:8501 myregistry.azurecr.io/azure-openai-portal:v1.1.0
```

### GitHub Container Registry (GHCR)

#### 配置 GHCR

```bash
# 1. 创建 Personal Access Token
# 访问 GitHub Settings > Developer settings > Personal access tokens
# 权限: write:packages, read:packages, delete:packages

# 2. 登录
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# 3. 构建并推送
./build-and-push.sh v1.1.0 ghcr.io/yourusername
```

#### 公开镜像

在 GitHub 仓库的 Package 设置中将镜像设置为 Public。

#### 从 GHCR 拉取

```bash
# 公开镜像（无需认证）
docker pull ghcr.io/yourusername/azure-openai-portal:v1.1.0

# 私有镜像（需要认证）
docker login ghcr.io
docker pull ghcr.io/yourusername/azure-openai-portal:v1.1.0
```

## 🎯 生产部署

### 环境变量配置

```bash
# 方式 1: 命令行传递
docker run -d \
  -p 8501:8501 \
  -e AZURE_OPENAI_API_KEY=your_key \
  -e AZURE_OPENAI_ENDPOINT=your_endpoint \
  -e AZURE_OPENAI_API_VERSION=2024-02-15-preview \
  --name azure-openai-portal \
  azure-openai-portal:latest

# 方式 2: 使用 env 文件
docker run -d \
  -p 8501:8501 \
  --env-file .env \
  --name azure-openai-portal \
  azure-openai-portal:latest

# 方式 3: Docker Compose
# 在 docker-compose.yml 中配置环境变量
```

### 健康检查

镜像内置健康检查：

```bash
# 检查容器健康状态
docker inspect --format='{{.State.Health.Status}}' azure-openai-portal

# 查看健康检查日志
docker inspect --format='{{json .State.Health}}' azure-openai-portal | jq
```

### 资源限制

```bash
# 限制资源使用
docker run -d \
  -p 8501:8501 \
  --memory="512m" \
  --cpus="1.0" \
  --name azure-openai-portal \
  azure-openai-portal:latest
```

## 📊 镜像信息

### 镜像大小

```bash
# 查看镜像大小
docker images azure-openai-portal

# 查看镜像层信息
docker history azure-openai-portal:latest
```

### 镜像扫描

```bash
# 使用 Docker Scout 扫描
docker scout quickview azure-openai-portal:latest

# 使用 Trivy 扫描
trivy image azure-openai-portal:latest
```

## 🔐 安全最佳实践

### 1. 不要在镜像中包含敏感信息

❌ 错误做法：
```dockerfile
ENV AZURE_OPENAI_API_KEY=sk-xxxxx
```

✅ 正确做法：
```bash
docker run -e AZURE_OPENAI_API_KEY=$API_KEY ...
```

### 2. 使用非 root 用户

镜像已配置为使用 `vscode` 用户运行。

### 3. 定期更新基础镜像

```bash
# 拉取最新的基础镜像
docker pull mcr.microsoft.com/devcontainers/python:3.11

# 重新构建
./build-and-push.sh
```

### 4. 镜像签名

```bash
# 使用 Docker Content Trust
export DOCKER_CONTENT_TRUST=1
docker push myregistry.azurecr.io/azure-openai-portal:v1.1.0
```

## 🚦 CI/CD 集成

### GitHub Actions

创建 `.github/workflows/docker.yml`：

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ghcr.io/${{ github.repository }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          file: .devcontainer/Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

### Azure DevOps

创建 `azure-pipelines.yml`：

```yaml
trigger:
  branches:
    include:
      - main
  tags:
    include:
      - v*

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: Docker@2
    inputs:
      containerRegistry: 'myACR'
      repository: 'azure-openai-portal'
      command: 'buildAndPush'
      Dockerfile: '.devcontainer/Dockerfile'
      tags: |
        $(Build.BuildId)
        latest
```

## 🛠️ 故障排查

### 构建失败

```bash
# 查看详细构建日志
docker build --no-cache --progress=plain -t azure-openai-portal:latest -f .devcontainer/Dockerfile .

# 检查 Dockerfile 语法
docker build --dry-run -f .devcontainer/Dockerfile .
```

### 容器无法启动

```bash
# 查看容器日志
docker logs azure-openai-portal

# 进入容器调试
docker exec -it azure-openai-portal bash

# 检查端口占用
netstat -tulpn | grep 8501
```

### 推送失败

```bash
# 重新登录
docker logout myregistry.azurecr.io
docker login myregistry.azurecr.io

# 检查网络连接
curl -I https://myregistry.azurecr.io

# 检查权限
docker info
```

## 📖 参考资源

- Docker 官方文档: https://docs.docker.com
- Azure Container Registry: https://docs.microsoft.com/azure/container-registry/
- GitHub Container Registry: https://docs.github.com/packages/working-with-a-github-packages-registry/working-with-the-container-registry
- Dev Containers: https://containers.dev

## 💡 常见使用场景

### 场景 1: 本地开发

```bash
# 使用 Dev Container
code .
# 选择 "Reopen in Container"
```

### 场景 2: 团队共享

```bash
# 推送到共享注册表
./build-and-push.sh v1.1.0 teamregistry.azurecr.io

# 团队成员拉取
docker pull teamregistry.azurecr.io/azure-openai-portal:v1.1.0
docker run -d -p 8501:8501 teamregistry.azurecr.io/azure-openai-portal:v1.1.0
```

### 场景 3: 生产部署

```bash
# 部署到 Azure Container Instances
az container create \
  --resource-group myResourceGroup \
  --name azure-openai-portal \
  --image myregistry.azurecr.io/azure-openai-portal:v1.1.0 \
  --dns-name-label my-portal \
  --ports 8501 \
  --environment-variables \
    AZURE_OPENAI_API_KEY=your_key \
    AZURE_OPENAI_ENDPOINT=your_endpoint
```

---

**版本**: 1.0  
**最后更新**: 2026-01-16
