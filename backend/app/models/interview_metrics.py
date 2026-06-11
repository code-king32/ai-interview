"""
面试指标追踪 —— token 消耗、延迟、Agent 调用统计。
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from app.database import Base


class InterviewMetrics(Base):
    __tablename__ = "interview_metrics"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    agent_name = Column(String(50))
    action = Column(String(50))  # question / score / followup / report
    latency_ms = Column(Float, default=0)
    tokens_used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
