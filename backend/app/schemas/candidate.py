from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    resume_text: Optional[str] = None
    resume_file_path: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    resume_text: Optional[str] = None
    resume_file_path: Optional[str] = None

class CandidateResponse(CandidateBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True