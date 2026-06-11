"""
知识增强服务 —— 将 JD + 简历拆解为知识点，面试时检索相关内容注入上下文。
"""
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class KnowledgePoint:
    """单个知识点。"""
    name: str
    category: str  # skill / project / concept / tool
    source: str    # jd / resume
    relevance: float = 1.0
    description: str = ""


class KnowledgeBase:
    """面试知识库 —— 从 JD 和简历中提取结构化知识点。"""

    # 技术关键词映射表
    TECH_MAP = {
        "java": {"category": "skill", "related": ["jvm", "spring", "多线程", "集合", "并发"]},
        "spring": {"category": "skill", "related": ["ioc", "aop", "boot", "mvc", "cloud", "事务"]},
        "mysql": {"category": "skill", "related": ["索引", "sql优化", "分库分表", "事务", "锁"]},
        "redis": {"category": "skill", "related": ["缓存", "分布式锁", "哨兵", "集群", "持久化"]},
        "docker": {"category": "tool", "related": ["容器", "k8s", "镜像", "编排"]},
        "k8s": {"category": "tool", "related": ["容器编排", "pod", "service", "deployment"]},
        "kubernetes": {"category": "tool", "related": ["容器编排", "pod", "service", "deployment"]},
        "python": {"category": "skill", "related": ["gil", "异步", "协程", "django", "fastapi"]},
        "vue": {"category": "skill", "related": ["响应式", "组件", "vite", "router", "pinia"]},
        "react": {"category": "skill", "related": ["hooks", "虚拟dom", "redux", "next.js"]},
        "typescript": {"category": "skill", "related": ["类型系统", "泛型", "接口", "装饰器"]},
        "微服务": {"category": "concept", "related": ["服务治理", "网关", "熔断", "链路追踪"]},
        "分布式": {"category": "concept", "related": ["cap", "一致性", "分布式事务", "raft"]},
        "高并发": {"category": "concept", "related": ["限流", "降级", "缓存", "异步", "队列"]},
        "性能优化": {"category": "concept", "related": ["jvm调优", "sql优化", "缓存策略", "索引"]},
        "jvm": {"category": "concept", "related": ["gc", "内存模型", "类加载", "调优"]},
        "mq": {"category": "tool", "related": ["消息队列", "kafka", "rabbitmq", "rocketmq"]},
        "elasticsearch": {"category": "tool", "related": ["倒排索引", "全文搜索", "聚合"]},
        "git": {"category": "tool", "related": ["分支管理", "ci/cd", "代码审查"]},
        "dd": {"category": "concept", "related": ["领域驱动设计", "聚合根", "限界上下文"]},
    }

    def __init__(self):
        self.points: list[KnowledgePoint] = []

    def build(self, jd_text: str, resume_text: str):
        """从 JD 和简历中构建知识库。"""
        self.points = []

        # 从 JD 提取
        self._extract(jd_text, "jd")
        # 从简历提取
        self._extract(resume_text, "resume")
        # 补全关联知识点
        self._expand_relations()
        # 去重
        self._deduplicate()

        return self

    def _extract(self, text: str, source: str):
        """从文本中提取知识点。"""
        text_lower = text.lower()
        for keyword, info in self.TECH_MAP.items():
            if keyword in text_lower:
                self.points.append(KnowledgePoint(
                    name=keyword,
                    category=info["category"],
                    source=source,
                    relevance=1.0,
                    description=info["related"][0] if info["related"] else "",
                ))

    def _expand_relations(self):
        """展开关联知识点。"""
        existing = {p.name for p in self.points}
        new_points = []
        for p in self.points:
            if p.name in self.TECH_MAP:
                for related in self.TECH_MAP[p.name]["related"]:
                    if related not in existing and len(related) > 1:
                        new_points.append(KnowledgePoint(
                            name=related,
                            category=self.TECH_MAP.get(related, {}).get("category", "concept"),
                            source=p.source,
                            relevance=0.7,
                            description="关联自: " + p.name,
                        ))
                        existing.add(related)
        self.points.extend(new_points)

    def _deduplicate(self):
        """去重——保留 relevance 最高的。"""
        seen: dict[str, KnowledgePoint] = {}
        for p in self.points:
            if p.name not in seen or p.relevance > seen[p.name].relevance:
                seen[p.name] = p
        self.points = sorted(seen.values(), key=lambda p: p.relevance, reverse=True)

    def search(self, topic: str, limit: int = 5) -> list[KnowledgePoint]:
        """根据当前话题检索相关知识点。"""
        topic_lower = topic.lower()
        scored: list[tuple[float, KnowledgePoint]] = []

        for p in self.points:
            score = 0.0
            if p.name in topic_lower:
                score = 1.0
            elif any(k in topic_lower for k in self.TECH_MAP.get(p.name, {}).get("related", [])):
                score = 0.5
            elif p.category in topic_lower:
                score = 0.3

            if score > 0:
                scored.append((score * p.relevance, p))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in scored[:limit]]

    def summary(self) -> str:
        """知识库摘要——注入到 AI 面试官的上下文中。"""
        skills = [p.name for p in self.points if p.category == "skill"]
        concepts = [p.name for p in self.points if p.category == "concept"]
        tools = [p.name for p in self.points if p.category == "tool"]
        resume_points = [p.name for p in self.points if p.source == "resume"]

        parts = []
        if skills:
            parts.append(f"核心技术栈：{'、'.join(skills[:8])}")
        if concepts:
            parts.append(f"涉及概念：{'、'.join(concepts[:6])}")
        if tools:
            parts.append(f"工具链：{'、'.join(tools[:6])}")
        if resume_points:
            parts.append(f"简历亮点：{'、'.join(resume_points[:6])}")

        return "；".join(parts) if parts else "暂无"

    def inject_context(self, topic: str) -> str:
        """注入相关知识点到面试上下文中。"""
        related = self.search(topic)
        if not related:
            return ""

        lines = ["## 相关知识点（供出题参考）"]
        for p in related:
            lines.append(f"- {p.name} ({p.category}, 来自{p.source}): {p.description}")
        return "\n".join(lines)
