from pydantic import BaseModel
from typing import Optional, List, Any, Dict


class ReportResponse(BaseModel):
    candidate: Optional[Dict[str, Any]] = None
    job: Optional[Dict[str, Any]] = None
    duration: Optional[str] = None
    total_questions: Optional[int] = None
    generated_at: Optional[str] = None
    overall_score: Optional[Dict[str, Any]] = None
    dimension_details: Optional[Dict[str, Any]] = None
    key_questions_summary: Optional[List[Dict[str, Any]]] = None
    question_details: Optional[List[Dict[str, Any]]] = None
    conversation: Optional[List[Dict[str, Any]]] = None
    next_steps: Optional[str] = None

    class Config:
        from_attributes = True
