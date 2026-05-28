"""
报告生成 Prompt —— 面试结束时调用，汇总全部问答生成终评。
"""

REPORT_PROMPT_TEMPLATE = """## 面试报告生成指令

请根据以下面试记录，生成一份结构化面试评估报告。

### 面试基本信息
- 岗位：{job_title}
- 候选人：{candidate_name}
- 面试时长：{duration}
- 共提问 {total_questions} 道题

### 面试问答记录
{qa_records}

### 报告输出格式
请严格按以下 JSON 格式输出（不要加 ```json 标记）：

{{
  "overall_score": {{
    "technical": 8.0,
    "communication": 7.5,
    "learning": 8.0,
    "match": 7.8,
    "recommendation": "推荐",
    "summary": "一段 200-300 字的综合评价，涵盖主要优势、不足和建议"
  }},
  "dimension_details": {{
    "technical": {{
      "score": 8.0,
      "strengths": ["优势1", "优势2"],
      "weaknesses": ["不足1"],
      "summary": "100字左右的技术能力小结"
    }},
    "communication": {{
      "score": 7.5,
      "strengths": ["优势1"],
      "weaknesses": [],
      "summary": "100字左右的沟通能力小结"
    }},
    "learning": {{
      "score": 8.0,
      "strengths": ["优势1"],
      "weaknesses": [],
      "summary": "100字左右的学习能力小结"
    }},
    "match": {{
      "score": 7.8,
      "strengths": ["优势1"],
      "weaknesses": ["不足1"],
      "summary": "100字左右的匹配度小结"
    }}
  }},
  "key_questions_summary": [
    {{
      "question": "Vue3 响应式原理",
      "answer_quality": "优秀|良好|一般|较差",
      "key_takeaway": "从回答中得到的关键判断"
    }}
  ],
  "next_steps": "建议进入终面 / 建议录用 / 建议补充笔试 / 不建议继续"
}}

### 注意事项
- 评分要有区分度，避免所有人都是中间分
- 优势和不足必须基于面试中真实展现的内容
- summary 要具体，不用套话
- 候选人完全没回答的问题，在 weaknesses 中标注"""


def build_report_prompt(
    job_title: str,
    candidate_name: str,
    duration: str,
    total_questions: int,
    qa_records: str,
) -> str:
    return REPORT_PROMPT_TEMPLATE.format(
        job_title=job_title,
        candidate_name=candidate_name,
        duration=duration,
        total_questions=total_questions,
        qa_records=qa_records,
    )
