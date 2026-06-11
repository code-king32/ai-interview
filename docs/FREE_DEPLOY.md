# 免费部署指南：Vercel + Railway

## 架构

```
用户 → https://ai-interview.vercel.app → 前端(Vercel)
                         ↓ /api/*
              → https://xxx.railway.app → 后端(Railway)
```

## 第一步：部署后端到 Railway（5 分钟）

1. 打开 https://railway.app → 用 GitHub 登录
2. 点击「New Project」→「Deploy from GitHub repo」
3. 选择 `code-king32/ai-interview`
4. Railway 自动检测到 `backend/` 目录下的 Python 项目
5. 设置 Root Directory 为 `backend`
6. 添加环境变量：
   - `ANTHROPIC_API_KEY` = 你的 Claude API Key
7. 等待部署完成，获得 URL 如 `https://ai-interview.up.railway.app`
8. 测试：`curl https://xxx.up.railway.app/api/health`

## 第二步：部署前端到 Vercel（5 分钟）

1. 打开 https://vercel.com → 用 GitHub 登录
2. 点击「Add New Project」→ 选择 `code-king32/ai-interview`
3. 设置 Root Directory 为 `frontend`
4. 设置环境变量：
   - `NUXT_PUBLIC_API_BASE` = `https://xxx.up.railway.app/api`（替换为第一步的 URL）
5. 点击 Deploy
6. 获得 URL 如 `https://ai-interview.vercel.app`

## 第三步：测试

1. 打开 `https://ai-interview.vercel.app/login`
2. 注册账号 → 登录 → 开始使用

## 更新代码

```bash
git push origin master  # Railway 和 Vercel 自动重新部署
```

## 免费额度

- Vercel：100GB 带宽 / 月，足够数千次访问
- Railway：$5 免费额度 / 月，约 500 小时运行时间
