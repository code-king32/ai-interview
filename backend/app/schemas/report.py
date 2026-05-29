from pydantic import BaseModel
from typing import Optional, List, Any, Dict


class ReportResponse(BaseModel):
    overall_score: Optional[Dict[str, Any]] = None
    dimension_details: Optional[Dict[str, Any]] = None
    key_questions_summary: Optional[List[Dict[str, Any]]] = None
    next_steps: Optional[str] = None

    class Config:
        from_attributes = True
