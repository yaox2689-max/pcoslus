"""PCOS Outcome CLI

Interactive tool for recording decision outcomes.
This is the most valuable data PCOS will ever collect.

Usage:
    python outcome_cli.py              # Interactive mode
    python outcome_cli.py pending      # Show pending outcomes
    python outcome_cli.py fill         # Fill a pending outcome
    python outcome_cli.py stats        # Show statistics
"""

import sys
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8001"


def show_pending():
    """Show all decisions waiting for outcome."""
    try:
        res = requests.get(f"{BASE_URL}/outcome/pending")
        res.raise_for_status()
        pending = res.json()
    except Exception as e:
        print(f"Error: {e}")
        return

    if not pending:
        print("\n  没有待记录的决策结果。")
        print("  继续使用 PCOS 做决策，30天后回来记录结果。")
        return

    print("\n" + "=" * 60)
    print("  待记录结果的决策")
    print("=" * 60)

    for i, p in enumerate(pending, 1):
        days = p["days_since"]
        reminder = " ⏰ 需要记录" if p["reminder_due"] else ""
        print(f"\n  [{i}] {p['question'][:50]}")
        print(f"      决策: {p['decision'][:60]}")
        print(f"      日期: {p['decision_date'][:10]} ({days}天前){reminder}")

    print("\n" + "=" * 60)


def fill_outcome():
    """Fill outcome for a pending decision."""
    try:
        res = requests.get(f"{BASE_URL}/outcome/pending")
        res.raise_for_status()
        pending = res.json()
    except Exception as e:
        print(f"Error: {e}")
        return

    if not pending:
        print("\n  没有待记录的决策。")
        return

    # Show list
    show_pending()

    # Select
    print("\n  选择要记录结果的决策 (输入编号): ")
    try:
        choice = int(input("  > ")) - 1
        if choice < 0 or choice >= len(pending):
            print("  无效选择")
            return
    except (ValueError, EOFError):
        print("  无效输入")
        return

    selected = pending[choice]
    print(f"\n  选中: {selected['question']}")
    print(f"  决策: {selected['decision']}")

    # Record outcome
    print("\n  ── 记录结果 ──\n")

    actual = input("  实际结果是什么? ").strip()
    if not actual:
        print("  取消")
        return

    print("  结果评分 (1=最差, 5=最好): ")
    try:
        score = int(input("  > "))
        if score < 1 or score > 5:
            print("  无效评分，使用 3")
            score = 3
    except (ValueError, EOFError):
        score = 3

    lesson = input("  学到了什么? (可选) ").strip() or None

    print("  惊喜程度 (1=预期中, 2=比预期好, 3=比预期差): ")
    try:
        surprise_choice = int(input("  > "))
        surprise = {1: "expected", 2: "better_than_expected", 3: "worse_than_expected"}.get(surprise_choice, "expected")
    except (ValueError, EOFError):
        surprise = "expected"

    # Identity update candidates
    candidates = []
    print("\n  这个结果是否暗示需要更新 Identity? (y/n)")
    try:
        if input("  > ").strip().lower() == 'y':
            print("  输入候选的 Identity 更新 (例如: optionality): ")
            cand_name = input("  > ").strip()
            if cand_name:
                candidates.append({
                    "name": cand_name,
                    "evidence": actual,
                    "confidence": 0.7,
                })
    except EOFError:
        pass

    # Send to API
    # First get the outcome_id from pending
    # We need to find the outcome_id from the decision
    try:
        res = requests.get(f"{BASE_URL}/outcome/stats")
        stats = res.json()

        # For now, we'll use the decision_id to find the outcome
        # In production, pending endpoint should return outcome_id
        print("\n  ⚠️  需要 outcome_id 才能记录。")
        print("  请使用 API 直接记录:")
        print(f"  PUT /outcome/{{outcome_id}}")
        print(f'  Body: {json.dumps({"actual_outcome": actual, "outcome_score": score, "lesson": lesson, "surprise": surprise, "identity_update_candidates": candidates}, ensure_ascii=False, indent=2)}')
    except Exception as e:
        print(f"  Error: {e}")


def show_stats():
    """Show outcome statistics."""
    try:
        res = requests.get(f"{BASE_URL}/outcome/stats")
        res.raise_for_status()
        stats = res.json()
    except Exception as e:
        print(f"Error: {e}")
        return

    print("\n" + "=" * 60)
    print("  Outcome 统计")
    print("=" * 60)
    print(f"\n  总决策数: {stats['total']}")
    print(f"  待记录:   {stats['pending']}")
    print(f"  已记录:   {stats['filled']}")
    print(f"  平均评分: {stats['avg_score'] or 'N/A'}")
    print("\n" + "=" * 60)


def interactive_mode():
    """Interactive menu."""
    print("\n" + "=" * 60)
    print("  🎯 PCOS Outcome Engine")
    print("=" * 60)
    print("\n  记录决策结果，让 PCOS 学习和进化\n")
    print("  [1] 查看待记录的决策")
    print("  [2] 记录决策结果")
    print("  [3] 查看统计")
    print("  [0] 退出\n")

    try:
        choice = input("  选择: ").strip()
    except EOFError:
        return

    if choice == "1":
        show_pending()
    elif choice == "2":
        fill_outcome()
    elif choice == "3":
        show_stats()
    elif choice == "0":
        print("  再见~")
    else:
        print("  无效选择")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "pending":
            show_pending()
        elif cmd == "fill":
            fill_outcome()
        elif cmd == "stats":
            show_stats()
        else:
            print(f"Unknown command: {cmd}")
            print("Usage: python outcome_cli.py [pending|fill|stats]")
    else:
        interactive_mode()
