from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    requirements = Column(Text)
    source = Column(String(20), default="seeker")  # "seeker" | "hr"
    created_at = Column(DateTime, default=datetime.utcnow)
