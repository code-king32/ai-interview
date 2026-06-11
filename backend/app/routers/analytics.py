"""
数据分析 API —— 面试统计、评分分布、Agent 效果评估。
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.interview import Interview, InterviewStatus
from app.models.message import Message, MessageRole
from app.models.interview_dataset import InterviewDataset

router = APIRouter()


@router.get("/analytics/overview")
def overview(db: Session = Depends(get_db)):
    """系统整体数据概览。"""
    total_interviews = db.query(Interview).count()
    completed = db.query(Interview).filter(
        Interview.status.in_([InterviewStatus.COMPLETED])
    ).count()

    total_messages = db.query(Message).count()
    ai_messages = db.query(Message).filter(Message.role == MessageRole.INTERVIEWER).count()
    avg_messages_per_interview = round(total_messages / max(total_interviews, 1), 1)

    # 平均评分（合并消息评分 + 数据集评分）
    avg_scores = {"correctness": 0, "depth": 0, "logic": 0, "practice": 0}
    all_scores = []
    # 从消息获取
    for m in db.query(Message).filter(Message.scores.isnot(None), Message.role == MessageRole.INTERVIEWER).all():
        if m.scores:
            all_scores.append(m.scores)
    # 从数据集获取
    for r in db.query(InterviewDataset).filter(InterviewDataset.scores.isnot(None)).all():
        if r.scores:
            all_scores.append(r.scores)
    if all_scores:
        for d in avg_scores:
            vals = [s.get(d, 0) for s in all_scores if d in s]
            avg_scores[d] = round(sum(vals) / len(vals), 1) if vals else 0

    return {
        "code": 0,
        "data": {
            "total_interviews": total_interviews,
            "completed_interviews": completed,
            "completion_rate": f"{completed / max(total_interviews, 1) * 100:.1f}%",
            "total_messages": total_messages,
            "avg_messages_per_interview": avg_messages_per_interview,
            "avg_scores": avg_scores,
        },
    }


@router.get("/analytics/scores/distribution")
def score_distribution(db: Session = Depends(get_db)):
    """评分分布 —— 各维度分数段统计。"""
    scored = db.query(Message).filter(
        Message.scores.isnot(None),
        Message.role == MessageRole.INTERVIEWER,
    ).all()

    dims = ["correctness", "depth", "logic", "practice"]
    distribution = {d: {"0-3": 0, "4-5": 0, "6-7": 0, "8-10": 0} for d in dims}

    for m in scored:
        for d in dims:
            val = m.scores.get(d, 0) if m.scores else 0
            if val <= 3:
                distribution[d]["0-3"] += 1
            elif val <= 5:
                distribution[d]["4-5"] += 1
            elif val <= 7:
                distribution[d]["6-7"] += 1
            else:
                distribution[d]["8-10"] += 1

    return {"code": 0, "data": distribution}


@router.get("/analytics/dataset/export")
def export_dataset(db: Session = Depends(get_db)):
    """导出面试数据集（Q&A对 + 评分）。"""
    records = db.query(InterviewDataset).order_by(InterviewDataset.created_at.desc()).all()
    return {
        "code": 0,
        "data": {
            "total": len(records),
            "records": [
                {
                    "job_title": r.job_title,
                    "topic": r.topic,
                    "question": r.question,
                    "answer": r.answer,
                    "scores": r.scores,
                    "answer_length": r.answer_length,
                    "prompt_version": r.prompt_version_used,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in records[:100]
            ],
        },
    }


@router.get("/analytics/dataset/export-finetune")
def export_finetune(db: Session = Depends(get_db)):
    """导出 JSONL 格式数据集，适配 OpenAI 微调。"""
    records = db.query(InterviewDataset).order_by(InterviewDataset.created_at.desc()).limit(500).all()

    lines = []
    for r in records:
        entry = {
            "messages": [
                {"role": "system", "content": f"你是技术面试评分专家。请对以下回答进行评分。岗位：{r.job_title}，话题：{r.topic}"},
                {"role": "user", "content": f"问题：{r.question}\n回答：{r.answer}"},
                {"role": "assistant", "content": str(r.scores) if r.scores else '{"correctness":0,"depth":0,"logic":0,"practice":0}'},
            ]
        }
        lines.append(entry)

    return {
        "code": 0,
        "data": {
            "format": "jsonl",
            "total": len(lines),
            "sample": lines[:3],
            "export_url": "/api/analytics/dataset/export",
        },
    }


@router.get("/analytics/dataset/stats")
def dataset_stats(db: Session = Depends(get_db)):
    """面试数据集统计。"""
    total = db.query(InterviewDataset).count()
    avg_length = db.query(func.avg(InterviewDataset.answer_length)).scalar() or 0

    # 按话题统计
    topics = (
        db.query(InterviewDataset.topic, func.count(InterviewDataset.id))
        .group_by(InterviewDataset.topic)
        .order_by(func.count(InterviewDataset.id).desc())
        .limit(20)
        .all()
    )

    # 按 Prompt 版本统计
    versions = (
        db.query(InterviewDataset.prompt_version_used, func.count(InterviewDataset.id))
        .group_by(InterviewDataset.prompt_version_used)
        .all()
    )

    return {
        "code": 0,
        "data": {
            "total_records": total,
            "avg_answer_length": round(float(avg_length), 1),
            "top_topics": [{"topic": t[0], "count": t[1]} for t in topics],
            "prompt_versions": [{"version": v[0], "count": v[1]} for v in versions],
        },
    }
