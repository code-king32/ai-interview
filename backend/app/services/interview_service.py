"""
面试核心服务 —— Claude API 调用、流式对话、消息处理的总调度。
"""

import json
import re
from typing import AsyncGenerator
from anthropic import AsyncAnthropic

from ..config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL
from ..prompts.system_prompt import build_system_prompt
from .question_service import build_question_instruction
from .scoring_service import parse_scores


class InterviewService:
    """面试会话管理器，封装 Claude API 调用、流式处理和状态管理。"""

    def __init__(self):
        self.client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    def _build_messages_for_api(
        self,
        system_prompt: str,
        history: list,
        candidate_answer: str,
        question_number: int,
        total_questions: int,
        covered_topics: list[str],
    ) -> list[dict]:
        """构建发送给 Claude API 的完整 messages 列表。"""
        messages = []

        # 注入出题指令作为 user 消息
        question_instruction = build_question_instruction(
            question_number=question_number + 1,  # 下一题的题号
            total_questions=total_questions,
            covered_topics=covered_topics,
        )

        # 构建对话历史
        for msg in history:
            role = "assistant" if msg.role == "interviewer" else "user"
            messages.append({"role": role, "content": msg.content})

        # 添加候选人最新回答
        messages.append({"role": "user", "content": candidate_answer})

        # 添加出题指令
        messages.append({"role": "user", "content": question_instruction})

        return messages

    async def send_message(
        self,
        candidate_answer: str,
        system_prompt: str,
        history: list,
        question_number: int,
        total_questions: int,
        covered_topics: list[str],
    ) -> dict:
        """发送候选人回答，获取 AI 面试官回复（非流式）。"""
        messages = self._build_messages_for_api(
            system_prompt, history, candidate_answer,
            question_number, total_questions, covered_topics,
        )

        response = await self.client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=4096,
            temperature=0.5,
            system=system_prompt,
            messages=messages,
        )

        return self._parse_ai_response(response.content[0].text)

    async def send_message_stream(
        self,
        candidate_answer: str,
        system_prompt: str,
        history: list,
        question_number: int,
        total_questions: int,
        covered_topics: list[str],
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """流式发送候选人回答，逐 token 产出 AI 回复。

        Yields:
            ("token", {"content": "文字片段"})  — 流式文本
            ("scores", {...})                   — 评分数据（如有）
            ("done", {"msg_id": 3, ...})        — 完成信号
            ("error", {"message": "..."})       — 错误
        """
        try:
            messages = self._build_messages_for_api(
                system_prompt, history, candidate_answer,
                question_number, total_questions, covered_topics,
            )

            full_content = ""
            async with self.client.messages.stream(
                model=ANTHROPIC_MODEL,
                max_tokens=4096,
                temperature=0.5,
                system=system_prompt,
                messages=messages,
            ) as stream:
                async for text_delta in stream.text_stream:
                    full_content += text_delta
                    yield ("token", {"content": text_delta})

            # 解析完整 AI 回复
            result = self._parse_ai_response(full_content)
            scores = result.get("scores")
            if scores:
                yield ("scores", scores)

            yield ("done", {
                "content": result["content"],
                "action": result["action"],
                "question_number": result.get("question_number"),
                "question_topic": result.get("question_topic"),
            })

        except Exception as e:
            yield ("error", {"message": str(e)})

    def _parse_ai_response(self, content: str) -> dict:
        """从 AI 回复中解析 JSON，处理各种格式异常。"""
        cleaned = content.strip()

        # 移除可能的 ```json ... ``` 包裹
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            # 尝试匹配 JSON 对象
            match = re.search(r"\{[\s\S]*\}", cleaned)
            if match:
                try:
                    data = json.loads(match.group())
                except json.JSONDecodeError:
                    data = {"action": "question", "content": content, "question_number": 1, "question_topic": "", "scores": None}
            else:
                data = {"action": "question", "content": content, "question_number": 1, "question_topic": "", "scores": None}

        # 标准化输出
        return {
            "action": data.get("action", "question"),
            "content": data.get("content", content),
            "question_number": data.get("question_number"),
            "question_topic": data.get("question_topic", ""),
            "scores": parse_scores(data.get("scores")),
        }
