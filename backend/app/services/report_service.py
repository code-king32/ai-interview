"""
报告生成服务 —— 调用 Claude API 生成终评报告。
"""

import json
from anthropic import AsyncAnthropic
from ..config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL
from ..prompts.report_prompts import build_report_prompt


async def generate_report(
    job_title: str,
    candidate_name: str,
    duration: str,
    total_questions: int,
    messages: list,
) -> dict:
    """汇总全部面试消息，调用 AI 生成结构化评估报告。"""

    # 构建 Q&A 记录文本
    qa_parts = []
    for msg in messages:
        if msg.role == "interviewer" and msg.question_number:
            # 找到对应的候选人回答
            answer = _find_answer(messages, msg.question_number)
            qa_parts.append(
                f"第{msg.question_number}题 | {msg.scores.get('topic', '')}\n"
                f"面试官：{msg.content}\n"
                f"候选人：{answer}\n"
            )
    qa_records = "\n---\n".join(qa_parts)

    prompt = build_report_prompt(
        job_title=job_title,
        candidate_name=candidate_name,
        duration=duration,
        total_questions=total_questions,
        qa_records=qa_records,
    )

    client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    response = await client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=4096,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}],
    )

    # 解析 AI 输出的 JSON
    content = response.content[0].text
    # 处理可能的 ```json ... ``` 包裹
    if "```" in content:
        content = content.split("```json")[-1].split("```")[0].strip()
    elif content.startswith("{") is False:
        # 尝试找到 JSON 起始位置
        idx = content.find("{")
        if idx != -1:
            content = content[idx:]

    return json.loads(content)


def _find_answer(messages: list, question_number: int) -> str:
    """从消息列表中查找指定题号的候选人回答。"""
    for msg in messages:
        if msg.role == "candidate" and msg.question_number == question_number:
            return msg.content
    return "（未找到回答）"
