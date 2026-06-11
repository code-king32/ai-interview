"""Prompt 管理 API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.prompt_manager import list_versions, toggle_version, seed_prompts

router = APIRouter()


@router.post("/prompts/seed")
def seed(db: Session = Depends(get_db)):
    """初始化 Prompt 种子数据。"""
    seed_prompts(db)
    return {"code": 0, "message": "种子数据已初始化"}


@router.get("/prompts/{agent_name}")
def get_prompts(agent_name: str, db: Session = Depends(get_db)):
    """获取某 Agent 的所有 Prompt 版本。"""
    if agent_name not in ("question", "scoring", "followup", "report"):
        raise HTTPException(status_code=400, detail="无效的 Agent 名称")
    return {"code": 0, "data": list_versions(db, agent_name)}


@router.put("/prompts/{version_id}/toggle")
def toggle(version_id: int, active: bool = True, db: Session = Depends(get_db)):
    """切换 Prompt 版本启用/禁用。"""
    pv = toggle_version(db, version_id, active)
    if not pv:
        raise HTTPException(status_code=404, detail="版本不存在")
    return {"code": 0, "message": f"版本 {pv.version} 已{'启用' if active else '禁用'}"}
