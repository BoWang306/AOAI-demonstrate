# Docker 部署指南

## 🐳 使用 Docker 运行应用

### 方法 1: Docker Compose (推荐)

#### 快速启动

```bash
# 进入项目目录
cd /path/to/webapp

# 使用 Docker Compose 启动
docker-compose -f .devcontainer/docker-compose.yml up -d

# 查看日志
docker-compose -f .devcontainer/docker-compose.yml logs -f

# 访问应用
# 打开浏览器访问: http://localhost:8501
```

#### 停止应用

```bash
# 停止容器
docker-compose -f .devcontainer/docker-compose.yml down

# 停止并删除数据
docker-compose -f .devcontainer/docker-compose.yml down -v
```

#### 重启应用

```bash
# 重启服务
docker-compose -f .devcontainer/docker-compose.yml restart

# 重新构建并启动
docker-compose -f .devcontainer/docker-compose.yml up -d --build
```

### 方法 2: Docker 命令

#### 构建镜像

```bash
# 在项目根目录构建
docker build -t azure-openai-portal -f .devcontainer/Dockerfile .
```

#### 运行容器

```bash
# 基本运行
docker run -d \
  --name azure-openai-portal \
  -p 8501:8501 \
  -v $(pwd):/workspace \
  azure-openai-portal

# 带环境变量运行
docker run -d \
  --name azure-openai-portal \
  -p 8501:8501 \
  -v $(pwd):/workspace \
  -e AZURE_OPENAI_API_KEY="your_key" \
  -e AZURE_OPENAI_ENDPOINT="your_endpoint" \
  azure-openai-portal

# 使用 .env 文件
docker run -d \
  --name azure-openai-portal \
  -p 8501:8501 \
  -v $(pwd):/workspace \
  --env-file .env \
  azure-openai-portal
```

#### 容器管理

```bash
# 查看运行中的容器
docker ps

# 查看日志
docker logs -f azure-openai-portal

# 进入容器
docker exec -it azure-openai-portal bash

# 停止容器
docker stop azure-openai-portal

# 删除容器
docker rm azure-openai-portal

# 删除镜像
docker rmi azure-openai-portal
```

## 🔧 配置环境变量

### 方法 1: 使用 .env 文件

```bash
# 创建 .env 文件
cp .env.example .env

# 编辑配置
nano .env

# 启动时自动加载
docker-compose -f .devcontainer/docker-compose.yml up -d
```

### 方法 2: 修改 docker-compose.yml

编辑 `.devcontainer/docker-compose.yml`：

```yaml
services:
  app:
    environment:
      - AZURE_OPENAI_API_KEY=your_key_here
      - AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
      - AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 方法 3: 使用宿主机环境变量

```bash
# 在宿主机设置环境变量
export AZURE_OPENAI_API_KEY="your_key"
export AZURE_OPENAI_ENDPOINT="your_endpoint"

# docker-compose.yml 中使用
environment:
  - AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}
  - AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT}

# 启动
docker-compose -f .devcontainer/docker-compose.yml up -d
```

## 📦 生产部署

### 优化的 Dockerfile

创建 `Dockerfile.prod`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 只安装生产依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app.py .
COPY config_helper.py .

# 非 root 用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
```

### 生产环境 docker-compose.yml

创建 `docker-compose.prod.yml`：

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    
    container_name: azure-openai-portal-prod
    
    ports:
      - "80:8501"
    
    environment:
      - AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}
      - AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT}
      - AZURE_OPENAI_API_VERSION=${AZURE_OPENAI_API_VERSION}
    
    restart: always
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### 使用生产配置部署

```bash
# 构建和启动
docker-compose -f docker-compose.prod.yml up -d --build

# 查看状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f
```

## 🌐 反向代理配置 (Nginx)

### nginx.conf

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

### 使用 Nginx Docker

```yaml
version: '3.8'

services:
  app:
    # ... (应用配置)
    expose:
      - "8501"
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      # SSL 证书（如果需要）
      # - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    networks:
      - app-network
    restart: always

networks:
  app-network:
    driver: bridge
```

## 🔍 监控和日志

### 查看实时日志

```bash
# 所有服务日志
docker-compose -f .devcontainer/docker-compose.yml logs -f

# 特定服务日志
docker-compose -f .devcontainer/docker-compose.yml logs -f app

# 最近 100 行日志
docker-compose -f .devcontainer/docker-compose.yml logs --tail=100 app
```

### 容器资源使用

```bash
# 查看资源使用情况
docker stats azure-openai-portal

# 查看容器详情
docker inspect azure-openai-portal
```

### 健康检查

```bash
# 检查容器健康状态
docker inspect --format='{{.State.Health.Status}}' azure-openai-portal

# 查看健康检查日志
docker inspect --format='{{json .State.Health}}' azure-openai-portal | jq
```

## 🐛 故障排查

### 容器无法启动

```bash
# 检查日志
docker logs azure-openai-portal

# 检查配置
docker-compose -f .devcontainer/docker-compose.yml config

# 重新构建
docker-compose -f .devcontainer/docker-compose.yml up -d --build --force-recreate
```

### 端口被占用

```bash
# 查看端口占用
lsof -i :8501
netstat -tlnp | grep 8501

# 更改端口
# 修改 docker-compose.yml 中的 ports 配置
ports:
  - "8502:8501"  # 宿主机:容器
```

### 环境变量未生效

```bash
# 检查环境变量
docker exec azure-openai-portal env | grep AZURE

# 进入容器调试
docker exec -it azure-openai-portal bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('AZURE_OPENAI_API_KEY'))"
```

### 性能问题

```bash
# 限制资源使用
docker run -d \
  --name azure-openai-portal \
  --memory="512m" \
  --cpus="1.0" \
  -p 8501:8501 \
  azure-openai-portal
```

或在 docker-compose.yml 中：

```yaml
services:
  app:
    # ...
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## 📚 常用命令速查

```bash
# 构建和启动
docker-compose up -d --build

# 停止
docker-compose down

# 重启
docker-compose restart

# 查看日志
docker-compose logs -f

# 进入容器
docker-compose exec app bash

# 更新镜像
docker-compose pull
docker-compose up -d

# 清理
docker-compose down -v --rmi all
docker system prune -a
```

## 🔐 安全建议

1. **不要在镜像中硬编码敏感信息**
2. **使用 Docker secrets 或环境变量**
3. **使用非 root 用户运行容器**
4. **定期更新基础镜像**
5. **限制容器资源使用**
6. **使用网络隔离**
7. **启用日志限制**

---

**Docker 部署完成！🐳**
