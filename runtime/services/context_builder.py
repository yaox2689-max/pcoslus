"""Context Builder

Loads RELEVANT identity and world model context for a decision.
Filters by topic to avoid loading everything.
"""

import re
from typing import Dict, Any, List, Set
from ..config import get_config
from ..models import IdentityContext, WorldModelContext


# Topic keywords mapping
TOPIC_KEYWORDS = {
    "funding": ["funding", "vc", "invest", "raise", "capital", "seed", "series", "融资", "投资"],
    "startup": ["startup", "founder", "pivot", "business", "company", "创业", "公司"],
    "product": ["product", "feature", "build", "mvp", "launch", "产品", "功能"],
    "market": ["market", "customer", "segment", "competition", "市场", "客户", "竞争"],
    "technology": ["tech", "ai", "llm", "model", "api", "技术", "模型"],
    "hiring": ["hire", "team", "cofounder", "employee", "招聘", "团队"],
    "resource": ["resource", "money", "time", "runway", "budget", "资源", "时间"],
    "growth": ["growth", "scale", "expand", "用户", "增长", "扩展"],
    "strategy": ["strategy", "direction", "focus", "战略", "方向"],
}


def extract_topics(question: str, context: str = None) -> Set[str]:
    """Extract relevant topics from question and context."""
    text = (question + " " + (context or "")).lower()
    topics = set()

    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                topics.add(topic)
                break

    # If no topics found, return all (fallback)
    if not topics:
        return set(TOPIC_KEYWORDS.keys())

    return topics


def filter_beliefs_by_topics(
    beliefs: List[Dict[str, Any]],
    topics: Set[str],
) -> List[Dict[str, Any]]:
    """Filter beliefs that are relevant to the given topics."""
    if not topics:
        return beliefs

    relevant = []
    for belief in beliefs:
        content = str(belief.get("content", "")).lower()
        # Check if any topic keyword appears in belief content
        for topic in topics:
            keywords = TOPIC_KEYWORDS.get(topic, [])
            for keyword in keywords:
                if keyword in content:
                    relevant.append(belief)
                    break
            else:
                continue
            break

    # If no beliefs match, return all (fallback)
    return relevant if relevant else beliefs


def filter_values_by_topics(
    values: List[str],
    topics: Set[str],
) -> List[str]:
    """Filter values that are relevant to the given topics."""
    # Map topics to relevant values
    topic_value_map = {
        "funding": ["自主性", "安全感", "autonomy", "security"],
        "startup": ["创造力", "自主性", "影响力", "creativity", "autonomy", "impact"],
        "product": ["创造力", "持续学习", "creativity", "learning"],
        "market": ["影响力", "持续学习", "impact", "learning"],
        "technology": ["持续学习", "创造力", "learning", "creativity"],
        "hiring": ["影响力", "自主性", "impact", "autonomy"],
        "resource": ["安全感", "自主性", "security", "autonomy"],
        "growth": ["影响力", "持续学习", "impact", "learning"],
        "strategy": ["自主性", "创造力", "autonomy", "creativity"],
    }

    relevant_values = set()
    for topic in topics:
        relevant_values.update(topic_value_map.get(topic, []))

    # Filter values
    filtered = [v for v in values if v in relevant_values]

    # If no values match, return all (fallback)
    return filtered if filtered else values


def build_identity_context(topics: Set[str] = None) -> IdentityContext:
    """Load identity context, filtered by topics."""
    config = get_config()

    values = config.get_identity_values()

    if topics:
        # For now, return all values but mark which are relevant
        # In v0.2, we'll filter more aggressively
        pass

    return IdentityContext(
        core_values=values,
        current_focus=config.get_identity_focus(),
        preferences=config.get_identity_preferences(),
    )


def build_world_model_context(
    question: str,
    context: str = None,
    topics: Set[str] = None,
) -> WorldModelContext:
    """Load relevant world model context for a decision."""
    config = get_config()

    if topics is None:
        topics = extract_topics(question, context)

    # Get beliefs and filter by topics
    all_beliefs = config.world_model.get("beliefs", [])
    relevant_beliefs = filter_beliefs_by_topics(all_beliefs, topics)

    # Get contradictions
    contradictions = config.world_model.get("contradictions", [])

    # Get blind spots
    blind_spots = config.world_model.get("blind_spots", [])

    # Calculate coverage score
    total_beliefs = len(all_beliefs)
    relevant_count = len(relevant_beliefs)
    if total_beliefs == 0:
        coverage_score = 0.0
    else:
        coverage_score = min(0.3 + (relevant_count / total_beliefs) * 0.5, 0.8)

    return WorldModelContext(
        relevant_beliefs=relevant_beliefs,
        contradictions=contradictions,
        blind_spots=blind_spots,
        coverage_score=coverage_score,
    )


def build_full_context(question: str, context: str = None) -> Dict[str, Any]:
    """Build full context for a decision with topic filtering."""
    topics = extract_topics(question, context)

    identity = build_identity_context(topics)
    world_model = build_world_model_context(question, context, topics)

    return {
        "identity": identity.model_dump(),
        "world_model": world_model.model_dump(),
        "topics": list(topics),
    }
