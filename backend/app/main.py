"""
FastAPI 入口 —— 挂载路由、配置 CORS、创建数据库表。
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import jobs_router, candidates_router, interviews_router, reports_router, auth_router, invite_router, analytics_router, prompts_router
from app.services.prompt_manager import seed_prompts
from app.database import SessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_prompts(db)
    finally:
        db.close()
    yield


app = FastAPI(title="AI 智能面试系统", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs_router, prefix="/api/jobs", tags=["岗位管理"])
app.include_router(candidates_router, prefix="/api/candidates", tags=["候选人管理"])
app.include_router(interviews_router, prefix="/api/interviews", tags=["面试会话"])
app.include_router(reports_router, prefix="/api/reports", tags=["面试报告"])
app.include_router(auth_router, prefix="/api/auth", tags=["用户认证"])
app.include_router(invite_router, prefix="/api", tags=["候选人邀请"])
app.include_router(analytics_router, prefix="/api", tags=["数据分析"])
app.include_router(prompts_router, prefix="/api", tags=["Prompt管理"])


@app.get("/api/health")
def health_check():
    return {"code": 0, "message": "ok"}
