"""PCOS Outcome Dashboard

Simple CLI dashboard to visualize outcome statistics.
Run: python outcome_dashboard.py

Shows:
- Total decisions / outcomes
- PCOS accuracy
- Good vs bad decisions
- Most successful values
- Pending outcomes
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8001"


def get_stats():
    """Get outcome statistics from API."""
    try:
        res = requests.get(f"{BASE_URL}/outcome/stats")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_filled_outcomes():
    """Get filled outcomes for analysis."""
    try:
        res = requests.get(f"{BASE_URL}/outcome/filled?limit=100")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_pending_outcomes():
    """Get pending outcomes."""
    try:
        res = requests.get(f"{BASE_URL}/outcome/pending")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error: {e}")
        return []


def analyze_outcomes(outcomes):
    """Analyze filled outcomes."""
    if not outcomes:
        return {}

    # Decision quality distribution
    quality_counts = {"good": 0, "neutral": 0, "bad": 0}
    for o in outcomes:
        q = o.get("decision_quality", "neutral")
        quality_counts[q] = quality_counts.get(q, 0) + 1

    # Outcome score distribution
    scores = [o["outcome_score"] for o in outcomes if o.get("outcome_score")]
    avg_score = sum(scores) / len(scores) if scores else 0

    # Controllability distribution
    control_counts = {"high": 0, "medium": 0, "low": 0}
    for o in outcomes:
        c = o.get("controllability", "medium")
        control_counts[c] = control_counts.get(c, 0) + 1

    # Surprise distribution
    surprise_counts = {"expected": 0, "better_than_expected": 0, "worse_than_expected": 0}
    for o in outcomes:
        s = o.get("surprise", "expected")
        surprise_counts[s] = surprise_counts.get(s, 0) + 1

    # Lessons learned
    lessons = [o["lesson"] for o in outcomes if o.get("lesson")]

    return {
        "quality": quality_counts,
        "avg_score": avg_score,
        "controllability": control_counts,
        "surprise": surprise_counts,
        "lessons": lessons,
    }


def print_dashboard():
    """Print the dashboard."""
    print("\n" + "=" * 60)
    print("  🎯 PCOS Outcome Dashboard")
    print("=" * 60)

    # Get stats
    stats = get_stats()
    if not stats:
        print("\n  ❌ 无法连接到 PCOS 服务")
        print("  请确保后端运行在 8001 端口")
        return

    # Basic stats
    print(f"\n  📊 总览")
    print(f"  {'─' * 40}")
    print(f"  总决策数:     {stats['total']}")
    print(f"  待记录:       {stats['pending']} ⏳")
    print(f"  已记录:       {stats['filled']} ✅")
    print(f"  待反思:       {stats['pending_reflections']} 🔄")

    if stats['avg_outcome_score']:
        print(f"\n  平均结果评分: {stats['avg_outcome_score']:.1f} / 5")

    # Decision quality
    if stats['good_decisions'] or stats['bad_decisions']:
        total_quality = stats['good_decisions'] + stats['bad_decisions']
        good_pct = (stats['good_decisions'] / total_quality * 100) if total_quality > 0 else 0
        print(f"\n  🎯 决策质量")
        print(f"  {'─' * 40}")
        print(f"  好决策: {stats['good_decisions']} ({good_pct:.0f}%)")
        print(f"  坏决策: {stats['bad_decisions']} ({100 - good_pct:.0f}%)")

    # Analyze filled outcomes
    outcomes = get_filled_outcomes()
    if outcomes:
        analysis = analyze_outcomes(outcomes)

        # Controllability
        print(f"\n  🎮 可控性分布")
        print(f"  {'─' * 40}")
        for level, count in analysis.get("controllability", {}).items():
            pct = (count / len(outcomes) * 100) if outcomes else 0
            bar = "█" * int(pct / 5)
            print(f"  {level:10} {bar} {count} ({pct:.0f}%)")

        # Surprise
        print(f"\n  😮 惊喜程度")
        print(f"  {'─' * 40}")
        for level, count in analysis.get("surprise", {}).items():
            pct = (count / len(outcomes) * 100) if outcomes else 0
            bar = "█" * int(pct / 5)
            label = {"expected": "预期中", "better_than_expected": "比预期好", "worse_than_expected": "比预期差"}.get(level, level)
            print(f"  {label:10} {bar} {count} ({pct:.0f}%)")

        # Lessons
        lessons = analysis.get("lessons", [])
        if lessons:
            print(f"\n  📚 学到的教训")
            print(f"  {'─' * 40}")
            for i, lesson in enumerate(lessons[:5], 1):
                print(f"  {i}. {lesson[:60]}")

    # Pending outcomes
    pending = get_pending_outcomes()
    if pending:
        print(f"\n  ⏳ 待记录结果")
        print(f"  {'─' * 40}")
        for p in pending[:5]:
            days = p['days_since']
            reminder = " ⏰" if p['reminder_due'] else ""
            print(f"  • {p['question'][:40]} ({days}天前){reminder}")
        if len(pending) > 5:
            print(f"  ... 还有 {len(pending) - 5} 个")

    # Progress
    print(f"\n  📈 进度")
    print(f"  {'─' * 40}")
    filled = stats['filled']
    if filled < 20:
        print(f"  目标: 20 个 Outcome (当前: {filled})")
        print(f"  {'█' * filled}{'░' * (20 - filled)} {filled}/20")
        print(f"  距离解锁 Reflection Engine 还需: {20 - filled} 个")
    else:
        print(f"  ✅ 已达到 20 个 Outcome!")
        print(f"  可以开始 Phase B: 分析阶段")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    print_dashboard()
