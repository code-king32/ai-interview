from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobBase(BaseModel):
    title: str
    description: Optional[str] = None
    requirements: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None

class JobResponse(JobBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True