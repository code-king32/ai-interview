from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Interview, Job, Candidate
from app.models.interview import InterviewStatus
from app.models.message import Message
from app.schemas import (
    InterviewCreate, InterviewResponse, InterviewUpdate,
    ChatRequest, ChatResponse, MessageResponse,
)
from app.services.interview_service import InterviewService
from app.services.report_service import ReportService

router = APIRouter()


@router.post("/", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
def create_interview(interview: InterviewCreate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == interview.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="职位不存在")
    candidate = db.query(Candidate).filter(Candidate.id == interview.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    new_interview = Interview(**interview.model_dump())
    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)
    return new_interview


@router.get("/", response_model=List[InterviewResponse])
def get_interviews(db: Session = Depends(get_db)):
    interviews = db.query(Interview).all()
    result = []
    for iv in interviews:
        data = {
            "id": iv.id, "job_id": iv.job_id, "candidate_id": iv.candidate_id,
            "status": iv.status, "started_at": iv.started_at,
            "completed_at": iv.completed_at, "overall_score": iv.overall_score,
        }
        job = db.query(Job).filter(Job.id == iv.job_id).first()
        candidate = db.query(Candidate).filter(Candidate.id == iv.candidate_id).first()
        data["job_title"] = job.title if job else None
        data["candidate_name"] = candidate.name if candidate else None
        result.append(data)
    return result


@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")
    return interview


@router.put("/{interview_id}", response_model=InterviewResponse)
def update_interview(interview_id: int, interview_update: InterviewUpdate, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")
    for key, value in interview_update.model_dump(exclude_unset=True).items():
        setattr(interview, key, value)
    db.commit()
    db.refresh(interview)
    return interview


@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")
    db.delete(interview)
    db.commit()
    return None


@router.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest, db: Session = Depends(get_db)):
    """发送消息获取 AI 回复（非流式）。"""
    service = InterviewService(db)
    try:
        result = await service.process_chat(chat_request.interview_id, chat_request.message)
        return ChatResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(chat_request: ChatRequest, db: Session = Depends(get_db)):
    """SSE 流式对话 —— 逐 token 推送 AI 回复。"""
    service = InterviewService(db)

    async def generate():
        try:
            async for chunk in service.process_chat_stream(
                chat_request.interview_id, chat_request.message
            ):
                yield chunk
        except ValueError as e:
            yield f"data: ERROR: {str(e)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/{interview_id}/end")
async def end_interview(interview_id: int, db: Session = Depends(get_db)):
    """结束面试，生成综合评分报告。"""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")
    if interview.status == InterviewStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="面试已结束")

    job = db.query(Job).filter(Job.id == interview.job_id).first()
    candidate = db.query(Candidate).filter(Candidate.id == interview.candidate_id).first()
    messages = (
        db.query(Message)
        .filter(Message.interview_id == interview_id)
        .order_by(Message.id)
        .all()
    )

    from datetime import datetime
    duration = "约30分钟"
    if interview.started_at:
        delta = datetime.utcnow() - interview.started_at
        minutes = int(delta.total_seconds() // 60)
        duration = f"约{minutes}分钟"

    try:
        report_service = ReportService(db)
        report = await report_service.generate(interview_id)
    except Exception:
        report = {
            "overall_score": {
                "technical": 0, "communication": 0, "learning": 0, "match": 0,
                "recommendation": "未生成", "summary": "AI 报告生成失败，请手动评估"
            },
            "dimension_details": {},
            "key_questions_summary": [],
            "next_steps": "",
        }

    interview.overall_score = report.get("overall_score", {})
    interview.status = InterviewStatus.COMPLETED
    interview.completed_at = datetime.utcnow()
    db.commit()

    return {"code": 0, "message": "success", "data": report}


@router.get("/{interview_id}/messages", response_model=List[MessageResponse])
def get_interview_messages(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")
    return sorted(interview.messages, key=lambda x: x.created_at)
