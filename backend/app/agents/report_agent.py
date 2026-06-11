"""
报告 Agent —— 基于面试记录生成综合评估报告。
"""
from .base import BaseAgent

REPORT_SYSTEM_PROMPT = """你是一名面试评估报告撰写专家。你根据候选人的面试记录，生成全面的评估报告。

## 输出格式（严格 JSON）
{
  "overall_score": {
    "technical": 8.5,
    "communication": 7.5,
    "learning": 8.0,
    "match": 7.8,
    "overall": 7.9
  },
  "summary": "200-300 字综合评价",
  "strengths": ["优势1", "优势2", "优势3"],
  "weaknesses": ["不足1", "不足2"],
  "suggestions": ["提升建议1", "提升建议2", "提升建议3"],
  "next_step": "下一步建议（如：建议进入终面 / 建议加强算法练习）"
}"""


class ReportAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReportAgent", REPORT_SYSTEM_PROMPT, temperature=0.3)

    async def generate(
        self,
        job_title: str,
        candidate_name: str,
        qa_records: str,
        scores_per_question: list[dict],
        duration: str,
        total_questions: int,
    ) -> dict:
        scores_text = "\n".join(
            f"第{i+1}题 {s.get('topic','')}: 正确性{s.get('correctness','?')} 深度{s.get('depth','?')} 逻辑{s.get('logic','?')} 实践{s.get('practice','?')} 评语:{s.get('comment','')}"
            for i, s in enumerate(scores_per_question)
        )

        msg = f"""岗位：{job_title}
候选人：{candidate_name}
面试时长：{duration}
共 {total_questions} 题

## 面试问答记录
{qa_records[:4000]}

## 每题评分
{scores_text}

请基于以上数据生成综合评估报告。"""
        return await self.call([{"role": "user", "content": msg}], max_tokens=4096)
