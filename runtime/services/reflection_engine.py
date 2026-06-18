"""Reflection Candidate Engine

Extracts patterns from outcomes and generates identity update candidates.
NEVER auto-updates identity - always requires human review.

This is NOT an auto-reflection engine. It's a candidate extraction engine.
Human review is mandatory before any identity change.
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import Counter
from dataclasses import dataclass, field

from .outcome_engine import get_filled_outcomes, get_outcome_stats


# ─────────────────────────────────────────────────────────────
# Data Models
# ─────────────────────────────────────────────────────────────

@dataclass
class PatternCandidate:
    """A pattern discovered from outcomes."""
    name: str
    description: str
    evidence_count: int
    success_rate: float
    confidence: float
    evidence_outcomes: List[str] = field(default_factory=list)
    status: str = "pending"  # pending | approved | rejected


@dataclass
class ValueInsight:
    """Insight about a value's performance."""
    value_name: str
    times_aligned: int
    avg_outcome_when_aligned: float
    avg_outcome_when_not_aligned: float
    insight: str


@dataclass
class ReflectionReport:
    """Complete reflection report."""
    generated_at: str
    total_outcomes: int
    filled_outcomes: int
    pattern_candidates: List[PatternCandidate]
    value_insights: List[ValueInsight]
    top_lessons: List[str]
    identity_update_candidates: List[Dict[str, Any]]


# ─────────────────────────────────────────────────────────────
# Pattern Detection
# ─────────────────────────────────────────────────────────────

def detect_decision_patterns(outcomes: List[Dict[str, Any]]) -> List[PatternCandidate]:
    """Detect recurring patterns from decision outcomes."""
    if len(outcomes) < 5:
        return []

    candidates = []

    # Pattern: Prefer optionality (choosing combination strategies)
    optionality_decisions = [
        o for o in outcomes
        if o.get("decision") and any(
            keyword in o["decision"].lower()
            for keyword in ["组合", "平衡", "同时", "both", "balance", "combine", "为主", "补充"]
        )
    ]
    if len(optionality_decisions) >= 2:
        success_scores = [o.get("outcome_score", 3) for o in optionality_decisions if o.get("outcome_score")]
        success_rate = sum(success_scores) / len(success_scores) / 5 if success_scores else 0.5
        candidates.append(PatternCandidate(
            name="prefer_optionality",
            description="倾向于选择组合策略，保留更多选择空间",
            evidence_count=len(optionality_decisions),
            success_rate=round(success_rate, 2),
            confidence=min(0.5 + len(optionality_decisions) * 0.1, 0.95),
            evidence_outcomes=[o["id"] for o in optionality_decisions],
        ))

    # Pattern: Action-oriented (choosing to act vs wait)
    action_decisions = [
        o for o in outcomes
        if o.get("decision") and any(
            keyword in o["decision"].lower()
            for keyword in ["立即", "马上", "开始", "接受", "参加", "做", "immediately", "start", "accept", "do"]
        )
    ]
    if len(action_decisions) >= 2:
        success_scores = [o.get("outcome_score", 3) for o in action_decisions if o.get("outcome_score")]
        success_rate = sum(success_scores) / len(success_scores) / 5 if success_scores else 0.5
        candidates.append(PatternCandidate(
            name="action_oriented",
            description="倾向于立即行动而非等待",
            evidence_count=len(action_decisions),
            success_rate=round(success_rate, 2),
            confidence=min(0.5 + len(action_decisions) * 0.1, 0.95),
            evidence_outcomes=[o["id"] for o in action_decisions],
        ))

    # Pattern: Growth-focused (choosing learning over safety)
    growth_decisions = [
        o for o in outcomes
        if o.get("decision") and any(
            keyword in o["decision"].lower()
            for keyword in ["学习", "新", "创新", "增长", "learn", "new", "innovate", "growth"]
        )
    ]
    if len(growth_decisions) >= 2:
        success_scores = [o.get("outcome_score", 3) for o in growth_decisions if o.get("outcome_score")]
        success_rate = sum(success_scores) / len(success_scores) / 5 if success_scores else 0.5
        candidates.append(PatternCandidate(
            name="growth_focused",
            description: "倾向于选择学习和成长机会",
            evidence_count=len(growth_decisions),
            success_rate=round(success_rate, 2),
            confidence=min(0.5 + len(growth_decisions) * 0.1, 0.95),
            evidence_outcomes=[o["id"] for o in growth_decisions],
        ))

    # Pattern: Independence-seeking (choosing autonomy over resources)
    independence_decisions = [
        o for o in outcomes
        if o.get("decision_quality") == "good" and any(
            keyword in o.get("decision", "").lower()
            for keyword in ["独立", "自主", "自己", "solo", "independent", "own"]
        )
    ]
    if len(independence_decisions) >= 2:
        candidates.append(PatternCandidate(
            name="independence_seeking",
            description: "倾向于保持独立和自主",
            evidence_count=len(independence_decisions),
            success_rate=0.7,
            confidence=min(0.5 + len(independence_decisions) * 0.1, 0.95),
            evidence_outcomes=[o["id"] for o in independence_decisions],
        ))

    # Pattern: PCOS influence pattern
    pcos_influenced = [
        o for o in outcomes
        if o.get("surprise") == "expected" and o.get("outcome_score", 0) >= 4
    ]
    if len(pcos_influenced) >= 3:
        candidates.append(PatternCandidate(
            name="pcos_aligned_decisions",
            description: "遵循 PCOS 建议的决策往往结果更好",
            evidence_count=len(pcos_influenced),
            success_rate=0.8,
            confidence=min(0.5 + len(pcos_influenced) * 0.05, 0.90),
            evidence_outcomes=[o["id"] for o in pcos_influenced],
        ))

    return candidates


# ─────────────────────────────────────────────────────────────
# Value Analysis
# ─────────────────────────────────────────────────────────────

def analyze_value_performance(outcomes: List[Dict[str, Any]]) -> List[ValueInsight]:
    """Analyze how different values correlate with outcomes."""
    if len(outcomes) < 5:
        return []

    # Count value occurrences in identity_update_candidates
    value_outcomes = {}
    for o in outcomes:
        candidates = o.get("identity_update_candidates", [])
        if isinstance(candidates, str):
            try:
                candidates = json.loads(candidates)
            except:
                candidates = []

        for cand in candidates:
            if isinstance(cand, dict):
                name = cand.get("name", "unknown")
                if name not in value_outcomes:
                    value_outcomes[name] = []
                value_outcomes[name].append(o.get("outcome_score", 3))

    insights = []
    for value_name, scores in value_outcomes.items():
        if len(scores) >= 2:
            avg_score = sum(scores) / len(scores)
            insights.append(ValueInsight(
                value_name=value_name,
                times_aligned=len(scores),
                avg_outcome_when_aligned=round(avg_score / 5, 2),
                avg_outcome_when_not_aligned=0.5,  # Default
                insight=f"{value_name} appears in {len(scores)} decisions with avg score {avg_score:.1f}/5",
            ))

    return insights


# ─────────────────────────────────────────────────────────────
# Lesson Extraction
# ─────────────────────────────────────────────────────────────

def extract_lessons(outcomes: List[Dict[str, Any]]) -> List[str]:
    """Extract lessons from filled outcomes."""
    lessons = []
    for o in outcomes:
        if o.get("lesson"):
            lessons.append(o["lesson"])
    return lessons[:10]  # Top 10


# ─────────────────────────────────────────────────────────────
# Main Reflection
# ─────────────────────────────────────────────────────────────

def generate_reflection_report() -> ReflectionReport:
    """Generate a complete reflection report from outcomes."""
    outcomes = get_filled_outcomes(limit=100)
    stats = get_outcome_stats()

    # Detect patterns
    patterns = detect_decision_patterns(outcomes)

    # Analyze values
    value_insights = analyze_value_performance(outcomes)

    # Extract lessons
    lessons = extract_lessons(outcomes)

    # Generate identity update candidates
    identity_candidates = []
    for pattern in patterns:
        if pattern.confidence >= 0.7 and pattern.evidence_count >= 3:
            identity_candidates.append({
                "name": pattern.name,
                "description": pattern.description,
                "evidence_count": pattern.evidence_count,
                "success_rate": pattern.success_rate,
                "confidence": pattern.confidence,
                "status": "pending_review",
                "recommendation": "approve" if pattern.success_rate > 0.6 else "review",
            })

    return ReflectionReport(
        generated_at=datetime.now().isoformat(),
        total_outcomes=stats["total"],
        filled_outcomes=stats["filled"],
        pattern_candidates=patterns,
        value_insights=value_insights,
        top_lessons=lessons,
        identity_update_candidates=identity_candidates,
    )


def get_pending_candidates() -> List[Dict[str, Any]]:
    """Get identity update candidates pending review."""
    report = generate_reflection_report()
    return [c for c in report.identity_update_candidates if c["status"] == "pending_review"]


def approve_candidate(candidate_name: str) -> bool:
    """Approve an identity update candidate.
    In v0.1, this just logs the approval. Actual identity update is manual.
    """
    # In production, this would update a database
    # For now, just return True
    print(f"[APPROVED] Identity candidate: {candidate_name}")
    print(f"  → Please manually update pcos/identity_data.yaml")
    return True


def reject_candidate(candidate_name: str, reason: str = None) -> bool:
    """Reject an identity update candidate."""
    print(f"[REJECTED] Identity candidate: {candidate_name}")
    if reason:
        print(f"  → Reason: {reason}")
    return True
