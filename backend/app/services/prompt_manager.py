"""
Prompt 版本管理器 —— 种子数据初始化、版本切换、A/B测试。
"""
from sqlalchemy.orm import Session
from ..models.prompt_version import PromptVersion


# 默认 Prompt 种子数据
SEED_PROMPTS = {
    "question": [
        {
            "version": "v1.0",
            "description": "基础出题：根据JD+简历生成题目",
            "prompt": """你是技术面试出题官。根据岗位要求和候选人背景生成一道面试题。
关联简历中的具体项目，难度递进，表达口语化。输出JSON: {question, topic, difficulty}""",
        },
        {
            "version": "v1.1",
            "description": "增强出题：加入知识库上下文",
            "prompt": """你是技术面试出题官。根据岗位要求、候选人背景和知识库上下文生成面试题。
必须关联简历中的具体项目，难度递进，偏好场景题。输出JSON: {question, topic, difficulty}""",
        },
    ],
    "scoring": [
        {
            "version": "v1.0",
            "description": "四维度评分",
            "prompt": """你是技术面试评分专家。对候选人回答进行4维度评分：
正确性、深度、逻辑、实践，每项0-10分。输出JSON: {correctness, depth, logic, practice, comment}""",
        },
    ],
    "followup": [
        {
            "version": "v1.0",
            "description": "追问判断",
            "prompt": """判断候选人回答是否需要追问。优秀→不追问，一般→追问1个深层问题，
模糊→追问具体场景。输出JSON: {should_follow_up, content}""",
        },
    ],
    "report": [
        {
            "version": "v1.0",
            "description": "综合报告生成",
            "prompt": """根据面试记录生成综合评估报告。输出JSON: {technical, communication, learning, match, summary, strengths, weaknesses, next_step}""",
        },
    ],
}


def seed_prompts(db: Session):
    """初始化 Prompt 版本种子数据。"""
    for agent_name, versions in SEED_PROMPTS.items():
        for v in versions:
            existing = db.query(PromptVersion).filter(
                PromptVersion.agent_name == agent_name,
                PromptVersion.version == v["version"],
            ).first()
            if not existing:
                pv = PromptVersion(
                    agent_name=agent_name,
                    version=v["version"],
                    system_prompt=v["prompt"],
                    description=v["description"],
                    is_active=1,
                )
                db.add(pv)
    db.commit()


def get_active_prompt(db: Session, agent_name: str, version: str | None = None) -> str | None:
    """获取活跃的 Prompt。如指定版本则取该版本。"""
    query = db.query(PromptVersion).filter(
        PromptVersion.agent_name == agent_name,
        PromptVersion.is_active == 1,
    )
    if version:
        query = query.filter(PromptVersion.version == version)
    pv = query.order_by(PromptVersion.created_at.desc()).first()
    return pv.system_prompt if pv else None


def list_versions(db: Session, agent_name: str) -> list:
    """列出某 Agent 的所有 Prompt 版本。"""
    versions = (
        db.query(PromptVersion)
        .filter(PromptVersion.agent_name == agent_name)
        .order_by(PromptVersion.created_at.desc())
        .all()
    )
    return [
        {
            "id": v.id,
            "version": v.version,
            "description": v.description,
            "is_active": bool(v.is_active),
            "created_at": v.created_at.isoformat() if v.created_at else None,
        }
        for v in versions
    ]


def toggle_version(db: Session, version_id: int, active: bool):
    """切换版本启用/禁用。"""
    pv = db.query(PromptVersion).filter(PromptVersion.id == version_id).first()
    if pv:
        pv.is_active = 1 if active else 0
        db.commit()
    return pv
