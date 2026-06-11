"""
出题 Agent —— 根据 JD + 简历 + 面试进度生成技术问题。
"""
from .base import BaseAgent

QUESTION_SYSTEM_PROMPT = """你是一名专业的技术面试出题官。你只需要做一件事：根据岗位要求和候选人背景，生成一道高质量的技术面试题。

## 出题原则
1. 必须关联候选人简历中的具体项目或技术栈，切忌泛泛而问
2. 问题要有明确的考察目标，偏好场景题 > 概念题
3. 难度递进，根据当前题号调整深度
4. 表达口语化，像真人面试官一样自然

## 输出格式（严格 JSON）
{
  "question": "面试题正文（口语化）",
  "topic": "考察的知识点名称",
  "difficulty": 3,
  "expected_points": ["期望候选人提到的要点1", "要点2"]
}

difficulty 范围 1-5：
1-2: 基础概念理解
3-4: 实践经验 + 技术深度
5: 系统设计 + 架构思维"""


class QuestionAgent(BaseAgent):
    def __init__(self):
        super().__init__("QuestionAgent", QUESTION_SYSTEM_PROMPT, temperature=0.6)

    async def generate(
        self,
        job_title: str,
        job_requirements: str,
        resume_text: str,
        question_number: int,
        total_questions: int,
        covered_topics: list[str],
    ) -> dict:
        topic_list = "、".join(covered_topics) if covered_topics else "无"
        msg = f"""岗位：{job_title}
技术要求：{job_requirements}
候选人背景：{resume_text[:1500]}

当前进度：第 {question_number}/{total_questions} 题
已考察知识点：{topic_list}

请生成第 {question_number} 题。难度应递进到 {min(5, 1 + question_number)} 级。"""
        return await self.call([{"role": "user", "content": msg}])
