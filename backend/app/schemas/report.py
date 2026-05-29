from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ReportSection(BaseModel):
    title: str
    content: str

class ReportResponse(BaseModel):
    interview_id: int
    candidate_name: str
    job_title: str
    overall_score: float
    sections: List[ReportSection]
    summary: str
    recommendation: str
    generated_at: datetime