"""PCOS Reflection CLI

Analyze outcomes and discover identity update candidates.

Usage:
    python reflection_cli.py              # Full report
    python reflection_cli.py candidates   # Show pending candidates
    python reflection_cli.py approve <name>  # Approve candidate
    python reflection_cli.py reject <name>   # Reject candidate
"""

import sys
import json
import requests

BASE_URL = "http://localhost:8001"


def show_report():
    """Show full reflection report."""
    try:
        res = requests.get(f"{BASE_URL}/reflection/report")
        res.raise_for_status()
        report = res.json()
    except Exception as e:
        print(f"Error: {e}")
        return

    print("\n" + "=" * 60)
    print("  🔍 PCOS Reflection Report")
    print("=" * 60)

    # Overview
    print(f"\n  📊 Overview")
    print(f"  {'─' * 40}")
    print(f"  Total outcomes: {report['total_outcomes']}")
    print(f"  Filled outcomes: {report['filled_outcomes']}")

    # Patterns
    patterns = report.get("pattern_candidates", [])
    if patterns:
        print(f"\n  🧩 Discovered Patterns")
        print(f"  {'─' * 40}")
        for p in patterns:
            conf = p['confidence']
            bar = "█" * int(conf * 20)
            print(f"\n  • {p['name']}")
            print(f"    {p['description']}")
            print(f"    Evidence: {p['evidence_count']} | Success: {p['success_rate']:.0%}")
            print(f"    Confidence: {bar} {conf:.0%}")
            print(f"    Status: {p['status']}")
    else:
        print(f"\n  🧩 No patterns discovered yet")
        print(f"  Need more outcomes (min 5)")

    # Value Insights
    insights = report.get("value_insights", [])
    if insights:
        print(f"\n  💎 Value Insights")
        print(f"  {'─' * 40}")
        for v in insights:
            print(f"  • {v['value_name']}: {v['insight']}")

    # Lessons
    lessons = report.get("top_lessons", [])
    if lessons:
        print(f"\n  📚 Top Lessons")
        print(f"  {'─' * 40}")
        for i, lesson in enumerate(lessons[:5], 1):
            print(f"  {i}. {lesson[:60]}")

    # Identity Candidates
    candidates = report.get("identity_update_candidates", [])
    if candidates:
        print(f"\n  🎯 Identity Update Candidates")
        print(f"  {'─' * 40}")
        for c in candidates:
            print(f"\n  • {c['name']}")
            print(f"    {c['description']}")
            print(f"    Evidence: {c['evidence_count']} | Success: {c['success_rate']:.0%}")
            print(f"    Confidence: {c['confidence']:.0%}")
            print(f"    Recommendation: {c['recommendation']}")
            print(f"    Status: {c['status']}")
    else:
        print(f"\n  🎯 No identity update candidates yet")

    print("\n" + "=" * 60)


def show_candidates():
    """Show pending candidates."""
    try:
        res = requests.get(f"{BASE_URL}/reflection/candidates")
        res.raise_for_status()
        candidates = res.json()
    except Exception as e:
        print(f"Error: {e}")
        return

    print("\n" + "=" * 60)
    print("  🎯 Pending Identity Update Candidates")
    print("=" * 60)

    if not candidates:
        print("\n  No pending candidates.")
        print("  Need more outcomes to generate candidates.")
        return

    for c in candidates:
        print(f"\n  • {c['name']}")
        print(f"    {c['description']}")
        print(f"    Evidence: {c['evidence_count']} | Success: {c['success_rate']:.0%}")
        print(f"    Confidence: {c['confidence']:.0%}")

    print("\n" + "=" * 60)
    print("\n  To approve: python reflection_cli.py approve <name>")
    print("  To reject:  python reflection_cli.py reject <name>")


def approve(name):
    """Approve a candidate."""
    try:
        res = requests.post(f"{BASE_URL}/reflection/candidates/approve",
                          json={"name": name})
        res.raise_for_status()
        result = res.json()
        print(f"\n  ✅ Approved: {name}")
        print(f"  → Please update pcos/identity_data.yaml manually")
    except Exception as e:
        print(f"Error: {e}")


def reject(name):
    """Reject a candidate."""
    reason = input(f"  Reason for rejecting '{name}': ").strip()
    try:
        res = requests.post(f"{BASE_URL}/reflection/candidates/reject",
                          json={"name": name, "reason": reason})
        res.raise_for_status()
        result = res.json()
        print(f"\n  ❌ Rejected: {name}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "candidates":
            show_candidates()
        elif cmd == "approve" and len(sys.argv) > 2:
            approve(sys.argv[2])
        elif cmd == "reject" and len(sys.argv) > 2:
            reject(sys.argv[2])
        else:
            print(f"Unknown command: {cmd}")
            print("Usage: python reflection_cli.py [candidates|approve|reject]")
    else:
        show_report()
