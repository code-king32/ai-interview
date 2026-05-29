from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.interview import InterviewStatus
from app.models.message import MessageRole

class InterviewBase(BaseModel):
    job_id: int
    candidate_id: int

class InterviewCreate(InterviewBase):
    pass

class InterviewUpdate(BaseModel):
    status: Optional[InterviewStatus] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    overall_score: Optional[float] = None

class InterviewResponse(InterviewBase):
    id: int
    status: InterviewStatus
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    overall_score: Optional[float]
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    interview_id: int
    message: str

class MessageResponse(BaseModel):
    id: int
    interview_id: int
    role: MessageRole
    content: str
    question_number: Optional[int]
    scores: Optional[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    user_message: str
    assistant_response: str
    message_id: int