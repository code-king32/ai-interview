"""
追问 Agent —— 判断是否需要对回答进行追问。
"""
from .base import BaseAgent

FOLLOWUP_SYSTEM_PROMPT = """你是一名技术面试追问专家。你的职责是分析候选人的回答，决定是否需要追问。

## 判断标准
- 回答优秀（概念准确 + 有深度 + 有量化数据）→ 不需要追问，给一个简短的正面过渡
- 回答一般（方向对但不够深入）→ 追问 1 个深层问题
- 回答模糊（只讲概念没有细节）→ 追问具体场景
- 回答错误（概念混淆或完全不懂）→ 追问是否了解相关基础

## 输出格式（严格 JSON）
{
  "should_follow_up": true,
  "follow_up_question": "追问内容（如果需要）",
  "transition": "过渡语（如果不需要追问，如：回答得很好，我们看下一题）"
}"""


class FollowUpAgent(BaseAgent):
    def __init__(self):
        super().__init__("FollowUpAgent", FOLLOWUP_SYSTEM_PROMPT, temperature=0.4)

    async def decide(self, question: str, answer: str, topic: str) -> dict:
        msg = f"""原题目（{topic}）：{question}

候选人回答：{answer[:2000]}

请判断是否需要追问。"""
        return await self.call([{"role": "user", "content": msg}])
