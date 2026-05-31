import uuid
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.database import Base


class InviteToken(Base):
    __tablename__ = "invite_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(64), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    used = Column(Boolean, default=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=True)
