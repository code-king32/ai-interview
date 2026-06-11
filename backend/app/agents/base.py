"""
Agent 基类 —— 封装 Claude API 调用、Tool Use 结构化输出、重试逻辑。
"""
import json
import re
from typing import Optional
from anthropic import AsyncAnthropic
from ..config import settings


class BaseAgent:
    """所有 Agent 的基类。"""

    def __init__(self, name: str, system_prompt: str, temperature: float = 0.5):
        self.name = name
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def call(self, messages: list[dict], max_tokens: int = 2048) -> dict:
        """调用 Claude，强制 JSON 输出，带重试。"""
        for attempt in range(3):
            try:
                response = await self.client.messages.create(
                    model=settings.ANTHROPIC_MODEL,
                    max_tokens=max_tokens,
                    temperature=self.temperature,
                    system=self.system_prompt,
                    messages=messages,
                )
                content = self._extract_text(response)
                return self._parse_json(content)
            except json.JSONDecodeError:
                if attempt == 2:
                    return {"error": "JSON 解析失败", "raw": getattr(response, 'content', '')}
            except Exception as e:
                if attempt == 2:
                    return {"error": str(e)}
        return {"error": "最大重试次数已耗尽"}

    async def call_raw(self, messages: list[dict], max_tokens: int = 2048) -> str:
        """调用 Claude，返回原始文本（非 JSON）。"""
        response = await self.client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=max_tokens,
            temperature=self.temperature,
            system=self.system_prompt,
            messages=messages,
        )
        return self._extract_text(response)

    def _extract_text(self, response) -> str:
        """从响应中提取文本块。"""
        for block in response.content:
            if block.type == "text" and block.text:
                return block.text
        return response.content[-1].text or ""

    def _parse_json(self, content: str) -> dict:
        """解析 JSON 响应，处理各种格式异常。"""
        cleaned = content.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\{[\s\S]*\}", cleaned)
            if match:
                return json.loads(match.group())
        raise json.JSONDecodeError("无法解析 JSON", cleaned, 0)


class ToolCallAgent(BaseAgent):
    """
    支持 Tool Use 的 Agent —— 强制模型调用定义好的工具函数。
    用于需要严格结构化输出的场景（评分、出题）。
    """

    def __init__(self, name: str, system_prompt: str, tools: list[dict], temperature: float = 0.3):
        super().__init__(name, system_prompt, temperature)
        self.tools = tools

    async def call_with_tool(self, messages: list[dict], tool_name: str, max_tokens: int = 2048) -> dict:
        """使用 Tool Use 调用 Claude，确保严格结构化输出。"""
        for attempt in range(3):
            try:
                response = await self.client.messages.create(
                    model=settings.ANTHROPIC_MODEL,
                    max_tokens=max_tokens,
                    temperature=self.temperature,
                    system=self.system_prompt,
                    tools=self.tools,
                    tool_choice={"type": "tool", "name": tool_name},
                    messages=messages,
                )
                # 提取 tool_use 内容
                for block in response.content:
                    if block.type == "tool_use" and block.name == tool_name:
                        return block.input or {}
                # 回退：尝试从文本解析 JSON
                text = self._extract_text(response)
                return self._parse_json(text)
            except Exception as e:
                if attempt == 2:
                    return {"error": str(e)}
        return {"error": "Tool call 失败"}
