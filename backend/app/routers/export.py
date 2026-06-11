"""
数据导出 API —— JSON / CSV / HTML 报告下载。
"""
import json
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.interview_dataset import InterviewDataset
from app.models.interview import Interview

router = APIRouter()


@router.get("/export/dataset/jsonl")
def export_jsonl(db: Session = Depends(get_db)):
    """导出 JSONL 格式数据集。"""
    records = db.query(InterviewDataset).order_by(InterviewDataset.created_at.desc()).limit(500).all()
    lines = []
    for r in records:
        entry = {
            "messages": [
                {"role": "system", "content": f"技术面试评分。岗位：{r.job_title}，话题：{r.topic}"},
                {"role": "user", "content": f"Q: {r.question}\nA: {r.answer}"},
                {"role": "assistant", "content": json.dumps(r.scores, ensure_ascii=False) if r.scores else "{}"},
            ]
        }
        lines.append(json.dumps(entry, ensure_ascii=False))

    content = "\n".join(lines)
    return Response(content=content, media_type="application/x-ndjson",
                    headers={"Content-Disposition": "attachment; filename=interview_dataset.jsonl"})


@router.get("/export/interviews/summary")
def export_summary(db: Session = Depends(get_db)):
    """导出面试摘要 CSV。"""
    interviews = db.query(Interview).order_by(Interview.id.desc()).limit(100).all()
    rows = ["id,status,job_id,candidate_id,score"]
    for iv in interviews:
        score_val = ""
        if iv.overall_score and isinstance(iv.overall_score, dict):
            dims = ["technical", "communication", "learning", "match"]
            vals = [iv.overall_score.get(d, 0) for d in dims]
            score_val = f"{sum(vals)/len(vals):.1f}" if vals else ""
        rows.append(f"{iv.id},{iv.status.value if hasattr(iv.status,'value') else iv.status},{iv.job_id},{iv.candidate_id},{score_val}")

    return Response(content="\n".join(rows), media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=interviews_summary.csv"})
