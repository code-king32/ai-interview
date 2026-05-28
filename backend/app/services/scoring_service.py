"""
评分引擎 —— 解析 AI 输出中的评分 JSON，提供评分校验和聚合。
"""

import json
from ..prompts.scoring_prompts import SCORING_RUBRICS


def parse_scores(raw_json: dict | None) -> dict | None:
    """从 AI 输出的 JSON 中提取并校验评分数据。"""
    if raw_json is None:
        return None

    required_dims = ["correctness", "depth", "logic", "practice"]
    for dim in required_dims:
        if dim not in raw_json:
            return None
        score = raw_json[dim]
        if not isinstance(score, (int, float)) or score < 0 or score > 10:
            return None

    return {
        "correctness": raw_json["correctness"],
        "depth": raw_json["depth"],
        "logic": raw_json["logic"],
        "practice": raw_json["practice"],
        "comment": raw_json.get("comment", ""),
    }


def aggregate_scores(scores_list: list[dict]) -> dict:
    """汇总所有单题评分，计算各维度平均分和综合分。"""
    if not scores_list:
        return {
            "technical": 0,
            "communication": 0,
            "learning": 0,
            "match": 0,
            "overall": 0,
        }

    n = len(scores_list)
    avg_correctness = sum(s.get("correctness", 0) for s in scores_list) / n
    avg_depth = sum(s.get("depth", 0) for s in scores_list) / n
    avg_logic = sum(s.get("logic", 0) for s in scores_list) / n
    avg_practice = sum(s.get("practice", 0) for s in scores_list) / n

    return {
        "technical": round(avg_correctness * 0.5 + avg_depth * 0.3 + avg_practice * 0.2, 1),
        "communication": round(avg_logic, 1),
        "learning": round(avg_depth * 0.4 + avg_correctness * 0.3 + avg_practice * 0.3, 1),
        "match": round(
            avg_correctness * 0.3 + avg_depth * 0.2 + avg_logic * 0.2 + avg_practice * 0.3, 1
        ),
        "overall": round(
            avg_correctness * 0.3 + avg_depth * 0.25 + avg_logic * 0.2 + avg_practice * 0.25, 1
        ),
    }
