# AI 面试系统 部署指南

## Docker 一键部署

```bash
# 1. 设置 API Key
echo "ANTHROPIC_API_KEY=sk-your-key" > backend/.env

# 2. 启动
docker-compose up -d

# 3. 访问
open http://localhost:3000
```

## 手动部署

### 后端
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 前端
```bash
cd frontend
npm install --registry=https://registry.npmmirror.com
npm run dev -- --host 0.0.0.0
```

## 云服务器部署（阿里云 ECS）

1. 安装 Docker `curl -fsSL https://get.docker.com | sh`
2. 克隆代码 `git clone https://github.com/code-king32/ai-interview.git`
3. 配置 `.env` 中的 API Key
4. `docker-compose up -d`
5. 配置 Nginx 反向代理 + SSL 证书
6. 域名解析到服务器 IP

## 技术栈
- 前端: Vue 3 + Nuxt 3 (SPA)
- 后端: Python FastAPI
- AI: Claude API (多 Agent 架构)
- 数据库: SQLite (可换 PostgreSQL)
