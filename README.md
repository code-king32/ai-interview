# AI 智能面试系统

双角色 AI 面试平台：求职者 AI 面试陪练 + HR 候选人管理系统。

## 技术亮点

- **多 Agent 架构**：出题/追问/评分/报告 4 个 AI Agent 协作，非单一 Prompt
- **Tool Use 结构化输出**：Claude Tool Use 强制 JSON，3 次重试防幻觉
- **Prompt 版本管理**：DB 存储 + A/B 测试，启动自动种子数据
- **RAG 知识增强**：JD/简历拆解为知识点，面试时检索注入上下文
- **数据集自动采集**：每次面试自动记录 QA 对 + 评分，支持 JSONL 导出微调
- **SSE 流式对话**：实时打字效果 + 评分即时反馈

## 快速开始

```bash
# 1. 配置 API Key
echo "ANTHROPIC_API_KEY=sk-your-key" > backend/.env

# 2. Docker 启动
docker-compose up -d

# 3. 打开
open http://localhost:3000
```

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3 + Nuxt 3 (SPA, SSR 关闭) |
| 后端 | Python FastAPI |
| AI | Claude API (多 Agent) |
| 数据库 | SQLite (可切 PostgreSQL) |
| 测试 | pytest (16 个测试) |
| 部署 | Docker Compose + ngrok |

## 项目结构

```
backend/
├── app/
│   ├── agents/          # 多 Agent AI 引擎
│   ├── services/        # 知识库、Prompt管理
│   ├── models/          # 8 个数据模型
│   ├── routers/         # 10 个 API 路由
│   └── middleware/       # 鉴权中间件
├── tests/               # 16 个测试
└── requirements.txt

frontend/
├── pages/               # 12 个页面
├── components/          # 6 个复用组件
├── stores/              # Pinia 状态管理
└── server/api/          # Nitro 代理
```

## 测试

```bash
cd backend
pip install pytest pytest-asyncio
python -m pytest -q
# 16 passed ✓
```

## API 端点

- `POST /api/auth/register` 注册
- `POST /api/auth/login` 登录
- `GET/POST/PUT/DELETE /api/jobs/` 岗位 CRUD
- `POST /api/interviews/chat-v2` Agent 对话
- `POST /api/interviews/{id}/end-v2` Agent 报告
- `GET /api/analytics/overview` 系统概览
- `GET /api/export/dataset/jsonl` 微调导出
- `GET /api/prompts/{agent}` Prompt 版本

## 部署

参见 [DEPLOY.md](DEPLOY.md) 和 [MIGRATION.md](backend/MIGRATION.md)
