from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class MessageRole(enum.Enum):
    INTERVIEWER = "interviewer"
    CANDIDATE = "candidate"
    SYSTEM = "system"

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    question_number = Column(Integer)
    scores = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    interview = relationship("Interview", back_populates="messages")