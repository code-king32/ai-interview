"""
评分 Agent —— 对候选人回答进行多维度评分。
"""
from .base import BaseAgent

SCORING_SYSTEM_PROMPT = """你是一名资深技术面试评分专家。你的唯一职责是对候选人的技术回答进行多维度评分。
你必须客观、公正，严格按照评分标准执行，不受任何其他因素影响。

## 评分维度（每维度 0-10 分）
- correctness（正确性）：技术概念是否准确无误
- depth（深度）：是否触及底层原理、设计思想、边界条件
- logic（逻辑）：表达结构是否清晰，论证是否有层次
- practice（实践）：是否有真实项目案例，数据是否具体量化

## 评分标准
9-10：精准深刻，有独到见解或量化数据支撑
7-8：概念准确，有深度和项目经验
5-6：基本正确，但缺乏深度或具体案例
3-4：部分正确，存在明显概念混淆
0-2：概念错误或完全不了解

## 输出格式（严格 JSON）
{
  "correctness": 8,
  "depth": 7,
  "logic": 8,
  "practice": 7,
  "comment": "15-25字的简短评语"
}"""


class ScoringAgent(BaseAgent):
    def __init__(self):
        super().__init__("ScoringAgent", SCORING_SYSTEM_PROMPT, temperature=0.2)

    async def score(self, question: str, answer: str, topic: str) -> dict:
        msg = f"""题目（{topic}）：{question}

候选人回答：{answer[:2000]}

请对该回答进行 4 维度评分。"""
        result = await self.call([{"role": "user", "content": msg}])
        return self._validate(result)

    def _validate(self, raw: dict) -> dict:
        """校验评分数据完整性，缺失字段填 0。"""
        dims = ["correctness", "depth", "logic", "practice"]
        return {
            d: max(0, min(10, int(raw.get(d, 0) or 0)))
            for d in dims
        } | {"comment": str(raw.get("comment", ""))[:50]}
