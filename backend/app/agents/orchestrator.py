"""
面试编排器 —— 协调出题、追问、评分、报告四个 Agent 完成完整面试流程。
"""
import json
from dataclasses import dataclass, field
from datetime import datetime

from .question_agent import QuestionAgent
from .scoring_agent import ScoringAgent
from .followup_agent import FollowUpAgent
from .report_agent import ReportAgent
from ..models.message import MessageRole


@dataclass
class InterviewSession:
    """面试会话状态。"""
    job_title: str
    job_requirements: str
    candidate_name: str
    resume_text: str
    total_questions: int = 5
    current_q: int = 0
    followup_count: int = 0
    covered_topics: list[str] = field(default_factory=list)
    scored_questions: list[dict] = field(default_factory=list)
    qa_history: list[dict] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def progress(self) -> str:
        return f"第 {self.current_q + 1}/{self.total_questions} 题"


class InterviewOrchestrator:
    """面试编排器 —— Agent 协调中心。"""

    def __init__(self):
        self.question_agent = QuestionAgent()
        self.scoring_agent = ScoringAgent()
        self.followup_agent = FollowUpAgent()
        self.report_agent = ReportAgent()

    async def start(self, session: InterviewSession) -> dict:
        """开场：生成第一个问题。"""
        return await self.question_agent.generate(
            job_title=session.job_title,
            job_requirements=session.job_requirements,
            resume_text=session.resume_text,
            question_number=1,
            total_questions=session.total_questions,
            covered_topics=[],
        )

    async def process_answer(
        self, session: InterviewSession, answer: str, question: str, topic: str
    ) -> dict:
        """
        处理候选人回答：
        1. 评分 Agent 对回答打分
        2. 追问 Agent 判断是否需要追问
        3. 需要追问则生成追问，否则出题 Agent 生成下一题
        """
        # 记录 QA
        session.qa_history.append({"question": question, "answer": answer, "topic": topic})

        # 1. 评分
        scores = await self.scoring_agent.score(question, answer, topic)
        scores["topic"] = topic
        session.scored_questions.append(scores)
        session.covered_topics.append(topic)

        # 2. 追问判断
        if session.followup_count < 2:
            followup = await self.followup_agent.decide(question, answer, topic)
            if followup.get("should_follow_up"):
                session.followup_count += 1
                return {
                    "action": "follow_up",
                    "content": followup.get("follow_up_question", "可以再详细说明一下吗？"),
                    "scores": scores,
                }

        # 3. 下一题
        session.current_q += 1
        session.followup_count = 0

        if session.current_q < session.total_questions:
            next_q = await self.question_agent.generate(
                job_title=session.job_title,
                job_requirements=session.job_requirements,
                resume_text=session.resume_text,
                question_number=session.current_q + 1,
                total_questions=session.total_questions,
                covered_topics=session.covered_topics,
            )
            return {
                "action": "next_question",
                "content": next_q.get("question", "请继续"),
                "topic": next_q.get("topic", ""),
                "scores": scores,
            }
        else:
            return {
                "action": "end",
                "content": "感谢你的参与！面试已结束。",
                "scores": scores,
                "is_last": True,
            }

    async def generate_report(self, session: InterviewSession) -> dict:
        """生成最终评估报告。"""
        delta = datetime.utcnow() - session.started_at
        duration = f"约{int(delta.total_seconds() // 60)}分钟"

        qa_text = "\n\n".join(
            f"第{i+1}题 [{qa['topic']}]\nQ: {qa['question']}\nA: {qa['answer'][:500]}"
            for i, qa in enumerate(session.qa_history)
        )

        return await self.report_agent.generate(
            job_title=session.job_title,
            candidate_name=session.candidate_name,
            qa_records=qa_text,
            scores_per_question=session.scored_questions,
            duration=duration,
            total_questions=session.total_questions,
        )
