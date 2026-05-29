from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class InterviewStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    status = Column(Enum(InterviewStatus), default=InterviewStatus.PENDING)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    overall_score = Column(Float)
    
    messages = relationship("Message", back_populates="interview")