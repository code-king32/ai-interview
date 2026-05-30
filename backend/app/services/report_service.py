"""
报告生成服务 —— 根据面试中的实际评分数据聚合生成报告。
"""
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Interview, Job, Candidate
from ..models.message import Message, MessageRole


class ReportService:
    """报告生成器 —— 基于实际面试数据聚合。"""

    def __init__(self, db: Session):
        self.db = db

    async def generate(self, interview_id: int) -> dict:
        interview = self.db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise ValueError("面试不存在")

        job = self.db.query(Job).filter(Job.id == interview.job_id).first()
        candidate = self.db.query(Candidate).filter(Candidate.id == interview.candidate_id).first()
        messages = (
            self.db.query(Message)
            .filter(Message.interview_id == interview_id)
            .order_by(Message.id)
            .all()
        )

        # 提取所有有评分的消息
        scored_messages = [m for m in messages if m.role == MessageRole.INTERVIEWER and m.scores and isinstance(m.scores, dict)]

        # 聚合各维度平均分
        dims = ["correctness", "depth", "logic", "practice"]
        dim_labels = {"correctness": "正确性", "depth": "深度", "logic": "逻辑", "practice": "实践"}
        aggregated = {d: 0.0 for d in dims}
        question_details = []

        for m in scored_messages:
            q_num = m.question_number or 0
            answer_msg = _find_answer(messages, q_num)
            sc = m.scores
            question_details.append({
                "question_number": q_num,
                "question": m.content[:200],
                "answer": answer_msg[:300] if answer_msg else "（未找到回答）",
                "scores": {d: sc.get(d, 0) for d in dims},
                "comment": sc.get("comment", ""),
            })
            for d in dims:
                if isinstance(sc.get(d), (int, float)):
                    aggregated[d] += sc[d]

        n = len(scored_messages) or 1
        for d in dims:
            aggregated[d] = round(aggregated[d] / n, 1)

        # 映射到报告维度
        tech = round((aggregated["correctness"] * 0.5 + aggregated["depth"] * 0.3 + aggregated["practice"] * 0.2), 1)
        comm = round(aggregated["logic"], 1)
        learn = round((aggregated["depth"] * 0.4 + aggregated["correctness"] * 0.3 + aggregated["practice"] * 0.3), 1)
        match_score = round((aggregated["correctness"] * 0.3 + aggregated["depth"] * 0.2 + aggregated["logic"] * 0.2 + aggregated["practice"] * 0.3), 1)

        # 录用建议
        overall = round((tech + comm + learn + match_score) / 4, 1)
        if overall >= 8.5:
            recommendation = "强烈推荐"
        elif overall >= 7:
            recommendation = "推荐"
        elif overall >= 5:
            recommendation = "保留"
        else:
            recommendation = "不推荐"

        # 计算时长
        duration = "约30分钟"
        if interview.started_at and interview.completed_at:
            minutes = int((interview.completed_at - interview.started_at).total_seconds() // 60)
            duration = f"约{minutes}分钟"
        elif interview.started_at:
            minutes = int((datetime.utcnow() - interview.started_at).total_seconds() // 60)
            duration = f"约{minutes}分钟"

        total_q = len([m for m in messages if m.role == MessageRole.INTERVIEWER])

        # 维度详情
        dimension_details = {
            "technical": {
                "score": tech,
                "strengths": _strengths("technical", tech),
                "weaknesses": _weaknesses("technical", tech),
                "summary": _dim_summary("technical", tech),
            },
            "communication": {
                "score": comm,
                "strengths": _strengths("communication", comm),
                "weaknesses": _weaknesses("communication", comm),
                "summary": _dim_summary("communication", comm),
            },
            "learning": {
                "score": learn,
                "strengths": _strengths("learning", learn),
                "weaknesses": _weaknesses("learning", learn),
                "summary": _dim_summary("learning", learn),
            },
            "match": {
                "score": match_score,
                "strengths": _strengths("match", match_score),
                "weaknesses": _weaknesses("match", match_score),
                "summary": _dim_summary("match", match_score),
            },
        }

        # 关键问答摘要
        key_questions_summary = []
        for qd in question_details[:5]:
            q_quality = "优秀" if qd["scores"].get("correctness", 0) >= 8 else ("良好" if qd["scores"].get("correctness", 0) >= 6 else "一般")
            key_questions_summary.append({
                "question": qd["question"][:100],
                "answer_quality": q_quality,
                "key_takeaway": qd.get("comment", f'正确性 {qd["scores"].get("correctness",0)}/10'),
            })

        # 综合评语
        if n >= 3:
            summary = f"候选人在本次技术面试中完成了 {total_q} 道题目的考察，综合评分 {overall} 分。"
            best_dim = max(dimension_details.items(), key=lambda x: x[1]["score"])
            worst_dim = min(dimension_details.items(), key=lambda x: x[1]["score"])
            summary += f"在{dim_label(best_dim[0])}方面表现最为突出（{best_dim[1]['score']}分），{dim_label(worst_dim[0])}方面仍有提升空间。"
            summary += f"整体评估：{recommendation}。"
        else:
            summary = f"候选人完成了 {total_q} 道题目。由于面试轮次较少，评分仅供参考。综合评估：{recommendation}。"

        return {
            "candidate": {"id": candidate.id, "name": candidate.name},
            "job": {"id": job.id, "title": job.title},
            "duration": duration,
            "total_questions": total_q,
            "generated_at": datetime.utcnow().isoformat(),
            "overall_score": {
                "technical": tech,
                "communication": comm,
                "learning": learn,
                "match": match_score,
                "recommendation": recommendation,
                "summary": summary,
            },
            "dimension_details": dimension_details,
            "key_questions_summary": key_questions_summary,
            "next_steps": _next_steps(recommendation),
        }


def _dim_label(k: str) -> str:
    return {"technical": "技术能力", "communication": "沟通表达", "learning": "学习潜力", "match": "岗位匹配"}.get(k, k)


def _strengths(k: str, score: float) -> list:
    if score >= 8:
        return [f"在{_dim_label(k)}维度的表现突出，展现了扎实的专业功底"]
    if score >= 7:
        return [f"{_dim_label(k)}能力良好，具备基本的岗位胜任力"]
    return []


def _weaknesses(k: str, score: float) -> list:
    if score < 6:
        return [f"{_dim_label(k)}方面建议加强专项训练和实践"]
    if score < 7:
        return [f"{_dim_label(k)}仍有提升空间，建议多做相关项目积累经验"]
    return []


def _dim_summary(k: str, score: float) -> str:
    if score >= 8:
        return f"该维度表现优秀，候选人具备较强的{_dim_label(k)}能力。"
    if score >= 7:
        return f"该维度表现良好，{_dim_label(k)}水平符合岗位基本要求。"
    return f"该维度有待提升，建议进一步强化{_dim_label(k)}相关技能。"


def _next_steps(recommendation: str) -> str:
    if recommendation == "强烈推荐":
        return "建议尽快安排终面或 HR 面，进一步考察候选人的团队协作和文化匹配度。"
    if recommendation == "推荐":
        return "建议进入下一轮面试，重点考察候选人在系统设计和项目管理方面的能力。"
    if recommendation == "保留":
        return "建议安排补充笔试或技术作业，进一步验证候选人在薄弱维度的实际水平。"
    return "当前评估结果不建议继续推进。如有特殊考虑，可安排加试。"


def _find_answer(messages: list, question_number: int) -> str | None:
    for msg in messages:
        if msg.role == MessageRole.CANDIDATE and msg.question_number == question_number:
            return msg.content
    return None
