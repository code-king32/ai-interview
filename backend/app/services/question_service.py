"""
出题引擎 —— 根据面试进度和已考察知识点，确定题目阶段并生成出题指令。
"""

STAGE_MAP = {
    1: "基础知识",
    2: "基础知识",
    3: "基础知识",
    4: "实践经验",
    5: "实践经验",
    6: "技术深度",
    7: "技术深度",
    8: "系统设计",
}


def get_current_stage(question_number: int, total_questions: int) -> str:
    """根据当前题号和总题数，映射到考察阶段。"""
    # 按比例映射
    if total_questions <= 5:
        ratio = question_number / total_questions
        if ratio <= 0.5:
            return "基础知识"
        if ratio <= 0.8:
            return "实践经验"
        return "技术深度"

    return STAGE_MAP.get(question_number, "技术深度")


def build_question_instruction(
    question_number: int,
    total_questions: int,
    covered_topics: list[str],
) -> str:
    """生成出题指令，注入到面试对话中。"""
    stage = get_current_stage(question_number, total_questions)
    covered = "、".join(covered_topics) if covered_topics else "（暂无）"

    return f"""## 出题指令

请生成第 {question_number} 道面试题。

已考察知识点：{covered}
当前阶段：{stage}
题目要求：{_stage_guide(stage)}

注意：题目应与已考察知识点不重复，使用口语化的中文提问。"""


def _stage_guide(stage: str) -> str:
    guides = {
        "基础知识": "考察核心概念理解，如'请解释 X 的工作原理'或'X 和 Y 有什么区别'",
        "实践经验": "考察项目中的实际应用，如'在项目中你如何解决 X 问题'或'踩过什么坑'",
        "技术深度": "考察底层原理和边界，如'X 在设计上有什么局限性'或'如果让你改进 X，你会怎么做'",
        "系统设计": "考察架构能力，如'请设计一个支持百万并发的 X 系统'或'你怎么做技术选型'",
    }
    return guides.get(stage, guides["基础知识"])
