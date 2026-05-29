from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, AsyncGenerator
from app.database import get_db
from app.models import Interview, Job, Candidate
from app.schemas import InterviewCreate, InterviewResponse, InterviewUpdate, ChatRequest, ChatResponse, MessageResponse
from app.services.interview_service import InterviewService
import asyncio

router = APIRouter()

@router.post("/", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
def create_interview(interview: InterviewCreate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == interview.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="职位不存在")
    
    candidate = db.query(Candidate).filter(Candidate.id == interview.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    
    new_interview = Interview(**interview.dict())
    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)
    return new_interview

@router.get("/", response_model=List[InterviewResponse])
def get_interviews(db: Session = Depends(get_db)):
    interviews = db.query(Interview).all()
    return interviews

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
    
    for key, value in interview_update.dict(exclude_unset=True).items():
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
def chat(chat_request: ChatRequest, db: Session = Depends(get_db)):
    interview_service = InterviewService(db)
    return interview_service.process_chat(chat_request.interview_id, chat_request.message)

@router.post("/chat/stream")
async def chat_stream(chat_request: ChatRequest, db: Session = Depends(get_db)):
    interview_service = InterviewService(db)
    
    async def generate() -> AsyncGenerator[str, None]:
        try:
            response = interview_service.process_chat(chat_request.interview_id, chat_request.message)
            
            for chunk in response.assistant_response:
                yield f"data: {chunk}\n\n"
                await asyncio.sleep(0.05)
            
            yield f"data: [DONE]\n\n"
        except Exception as e:
            yield f"data: ERROR: {str(e)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.get("/{interview_id}/messages", response_model=List[MessageResponse])
def get_interview_messages(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面试不存在")
    return sorted(interview.messages, key=lambda x: x.created_at)
