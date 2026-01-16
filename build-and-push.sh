#!/bin/bash

# Azure OpenAI 模型测试门户 - Docker 镜像构建和推送脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
IMAGE_NAME="azure-openai-portal"
VERSION=${1:-"latest"}
REGISTRY=${2:-""}  # 可选：容器注册表地址

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Azure OpenAI 模型测试门户${NC}"
echo -e "${BLUE}Docker 镜像构建脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 显示配置
echo -e "${GREEN}配置信息:${NC}"
echo -e "  镜像名称: ${IMAGE_NAME}"
echo -e "  版本标签: ${VERSION}"
if [ -n "$REGISTRY" ]; then
    echo -e "  容器注册表: ${REGISTRY}"
    FULL_IMAGE_NAME="${REGISTRY}/${IMAGE_NAME}"
else
    echo -e "  容器注册表: 本地构建（未指定注册表）"
    FULL_IMAGE_NAME="${IMAGE_NAME}"
fi
echo ""

# 构建镜像
echo -e "${YELLOW}步骤 1/4: 构建 Docker 镜像...${NC}"
docker build \
    -t "${FULL_IMAGE_NAME}:${VERSION}" \
    -t "${FULL_IMAGE_NAME}:latest" \
    -f .devcontainer/Dockerfile \
    .

echo -e "${GREEN}✅ 镜像构建成功${NC}"
echo ""

# 显示镜像信息
echo -e "${YELLOW}步骤 2/4: 镜像信息${NC}"
docker images "${FULL_IMAGE_NAME}" | head -n 2
echo ""

# 测试镜像
echo -e "${YELLOW}步骤 3/4: 测试镜像...${NC}"
echo "启动测试容器..."
CONTAINER_ID=$(docker run -d --rm -p 8502:8501 "${FULL_IMAGE_NAME}:${VERSION}")
echo "容器 ID: ${CONTAINER_ID}"

# 等待应用启动
echo "等待应用启动（10秒）..."
sleep 10

# 检查健康状态
if docker exec "${CONTAINER_ID}" curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 健康检查通过${NC}"
else
    echo -e "${RED}❌ 健康检查失败${NC}"
    docker logs "${CONTAINER_ID}"
    docker stop "${CONTAINER_ID}"
    exit 1
fi

# 停止测试容器
echo "停止测试容器..."
docker stop "${CONTAINER_ID}"
echo -e "${GREEN}✅ 镜像测试成功${NC}"
echo ""

# 推送到注册表（如果指定了）
if [ -n "$REGISTRY" ]; then
    echo -e "${YELLOW}步骤 4/4: 推送到容器注册表...${NC}"
    
    # 推送版本标签
    echo "推送 ${FULL_IMAGE_NAME}:${VERSION}..."
    docker push "${FULL_IMAGE_NAME}:${VERSION}"
    
    # 推送 latest 标签
    echo "推送 ${FULL_IMAGE_NAME}:latest..."
    docker push "${FULL_IMAGE_NAME}:latest"
    
    echo -e "${GREEN}✅ 镜像推送成功${NC}"
    echo ""
    echo -e "${GREEN}镜像已推送到:${NC}"
    echo -e "  ${FULL_IMAGE_NAME}:${VERSION}"
    echo -e "  ${FULL_IMAGE_NAME}:latest"
else
    echo -e "${YELLOW}步骤 4/4: 跳过推送（未指定容器注册表）${NC}"
    echo ""
    echo -e "${BLUE}本地镜像已准备就绪:${NC}"
    echo -e "  ${FULL_IMAGE_NAME}:${VERSION}"
    echo -e "  ${FULL_IMAGE_NAME}:latest"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ 完成！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 使用说明
echo -e "${BLUE}使用方法:${NC}"
echo ""
echo -e "${YELLOW}1. 本地运行:${NC}"
echo -e "   docker run -d -p 8501:8501 --name azure-openai-portal ${FULL_IMAGE_NAME}:${VERSION}"
echo ""
echo -e "${YELLOW}2. 使用环境变量:${NC}"
echo -e "   docker run -d -p 8501:8501 \\"
echo -e "     -e AZURE_OPENAI_API_KEY=your_key \\"
echo -e "     -e AZURE_OPENAI_ENDPOINT=your_endpoint \\"
echo -e "     ${FULL_IMAGE_NAME}:${VERSION}"
echo ""
echo -e "${YELLOW}3. 使用 Docker Compose:${NC}"
echo -e "   docker-compose up -d"
echo ""

if [ -n "$REGISTRY" ]; then
    echo -e "${YELLOW}4. 从注册表拉取:${NC}"
    echo -e "   docker pull ${FULL_IMAGE_NAME}:${VERSION}"
    echo ""
fi

echo -e "${BLUE}访问应用: http://localhost:8501${NC}"
echo ""
