"""
Agent Tool 定义 —— 用于 Anthropic Tool Use 强制结构化输出。
"""

# 评分工具
SCORE_TOOL = {
    "name": "submit_scores",
    "description": "提交对候选人回答的多维度评分",
    "input_schema": {
        "type": "object",
        "properties": {
            "correctness": {
                "type": "integer",
                "description": "技术概念准确度 (0-10)",
                "minimum": 0, "maximum": 10,
            },
            "depth": {
                "type": "integer",
                "description": "技术深度：是否触及底层原理 (0-10)",
                "minimum": 0, "maximum": 10,
            },
            "logic": {
                "type": "integer",
                "description": "表达逻辑和结构 (0-10)",
                "minimum": 0, "maximum": 10,
            },
            "practice": {
                "type": "integer",
                "description": "实践经验：是否有项目案例和数据 (0-10)",
                "minimum": 0, "maximum": 10,
            },
            "comment": {
                "type": "string",
                "description": "15-25字简短评语",
                "maxLength": 50,
            },
        },
        "required": ["correctness", "depth", "logic", "practice", "comment"],
    },
}

# 出题工具
QUESTION_TOOL = {
    "name": "submit_question",
    "description": "提交一道面试题",
    "input_schema": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "面试题正文（口语化）",
                "maxLength": 300,
            },
            "topic": {
                "type": "string",
                "description": "考察的知识点名称",
            },
            "difficulty": {
                "type": "integer",
                "description": "难度 1-5",
                "minimum": 1, "maximum": 5,
            },
        },
        "required": ["question", "topic", "difficulty"],
    },
}

# 追问判断工具
FOLLOWUP_TOOL = {
    "name": "decide_followup",
    "description": "判断是否需要追问以及追问内容",
    "input_schema": {
        "type": "object",
        "properties": {
            "should_follow_up": {
                "type": "boolean",
                "description": "是否需要追问",
            },
            "content": {
                "type": "string",
                "description": "追问内容或过渡语",
                "maxLength": 200,
            },
        },
        "required": ["should_follow_up", "content"],
    },
}

# 报告工具
REPORT_TOOL = {
    "name": "submit_report",
    "description": "提交综合评估报告",
    "input_schema": {
        "type": "object",
        "properties": {
            "technical": {"type": "number", "minimum": 0, "maximum": 10},
            "communication": {"type": "number", "minimum": 0, "maximum": 10},
            "learning": {"type": "number", "minimum": 0, "maximum": 10},
            "match": {"type": "number", "minimum": 0, "maximum": 10},
            "summary": {"type": "string", "maxLength": 500},
            "strengths": {"type": "array", "items": {"type": "string"}},
            "weaknesses": {"type": "array", "items": {"type": "string"}},
            "next_step": {"type": "string", "maxLength": 200},
        },
        "required": ["technical", "communication", "learning", "match", "summary"],
    },
}


def get_tool(name: str) -> dict:
    """根据名称返回 Tool 定义。"""
    tools = {
        "score": [SCORE_TOOL],
        "question": [QUESTION_TOOL],
        "followup": [FOLLOWUP_TOOL],
        "report": [REPORT_TOOL],
    }
    return tools.get(name, [])
