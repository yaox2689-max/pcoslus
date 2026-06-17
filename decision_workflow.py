"""PCOS Decision Workflow

Interactive workflow for recording real decisions and comparing with PCOS.
"""

import requests
import json
from datetime import datetime


BASE_URL = "http://localhost:8001"


def ask_pcos(question: str, context: str = None) -> dict:
    """Ask PCOS for a decision recommendation."""
    payload = {"question": question}
    if context:
        payload["context"] = context

    response = requests.post(f"{BASE_URL}/decide/", json=payload)
    return response.json()


def calculate_decision_alignment(pcos_result: dict, actual_decision: str) -> float:
    """Calculate alignment between PCOS recommendation and user's actual decision.

    Returns a score from 0.0 (complete mismatch) to 1.0 (perfect match).
    Uses semantic analysis, not string comparison.
    """
    pcos_rec = pcos_result.get("recommendation", "").lower()
    actual = actual_decision.lower()

    # Extract key concepts from both
    pcos_concepts = extract_concepts(pcos_rec)
    actual_concepts = extract_concepts(actual)

    if not pcos_concepts or not actual_concepts:
        return 0.5  # Can't determine

    # Calculate overlap
    overlap = pcos_concepts & actual_concepts
    total = pcos_concepts | actual_concepts

    if not total:
        return 0.5

    return len(overlap) / len(total)


def extract_concepts(text: str) -> set:
    """Extract key concepts from text."""
    concepts = set()

    # Direction keywords
    direction_map = {
        "ai": ["ai", "人工智能", "机器学习", "ml"],
        "java": ["java", "后端", "backend"],
        "python": ["python"],
        "product": ["产品", "product"],
        "consulting": ["咨询", "consulting", "外包"],
        "learn": ["学习", "learn", "学"],
        "build": ["做", "build", "开发", "创建"],
        "hire": ["招聘", "hire", "找"],
        "raise": ["融资", "raise", "投资"],
        "focus": ["专注", "focus", "全力"],
        "balance": ["平衡", "balance", "同时", "再", "补充"],
    }

    text_lower = text.lower()
    for concept, keywords in direction_map.items():
        if any(kw in text_lower for kw in keywords):
            concepts.add(concept)

    return concepts


def extract_decision_direction(text: str) -> str:
    """Extract the direction of a decision: positive, negative, or neutral.

    Returns:
        "positive": accepting, doing, moving forward
        "negative": rejecting, avoiding, not doing
        "neutral": balanced, hedging, combination
    """
    text_lower = text.lower()

    # Strong negative indicators
    negative_patterns = [
        "不", "不要", "拒绝", "不做", "不接受", "不转", "不融",
        "no", "don't", "reject", "decline", "not", "avoid",
        "保持", "维持", "继续", "keep", "maintain", "stay",
    ]

    # Strong positive indicators
    positive_patterns = [
        "要", "做", "接受", "转", "融", "学ai", "学 ai",
        "yes", "accept", "do", "pivot", "raise", "learn ai",
        "全力", "专注", "focus on",
    ]

    # Neutral/hedge indicators
    neutral_patterns = [
        "同时", "再", "补充", "平衡", "组合", "部分",
        "both", "and", "balance", "combine", "partial",
        "为主", "为辅", "先", "后",
    ]

    # Count matches
    negative_count = sum(1 for p in negative_patterns if p in text_lower)
    positive_count = sum(1 for p in positive_patterns if p in text_lower)
    neutral_count = sum(1 for p in neutral_patterns if p in text_lower)

    # Determine direction
    if neutral_count > 0 and (positive_count > 0 or negative_count > 0):
        return "neutral"  # Combination/hedge strategy
    elif negative_count > positive_count:
        return "negative"
    elif positive_count > negative_count:
        return "positive"
    else:
        return "neutral"


def calculate_decision_alignment(pcos_result: dict, actual_decision: str) -> float:
    """Calculate alignment between PCOS recommendation and user's actual decision.

    Returns a score from 0.0 (complete mismatch) to 1.0 (perfect match).
    Uses direction-based analysis, not string comparison.
    """
    pcos_rec = pcos_result.get("recommendation", "")
    actual = actual_decision

    # Extract directions
    pcos_direction = extract_decision_direction(pcos_rec)
    actual_direction = extract_decision_direction(actual)

    # Extract concepts for detailed comparison
    pcos_concepts = extract_concepts(pcos_rec.lower())
    actual_concepts = extract_concepts(actual.lower())

    # Direction match is primary
    if pcos_direction == actual_direction:
        direction_score = 1.0
    elif pcos_direction == "neutral" or actual_direction == "neutral":
        direction_score = 0.6  # Partial match
    else:
        direction_score = 0.0  # Opposite directions

    # Concept overlap is secondary
    if pcos_concepts and actual_concepts:
        overlap = pcos_concepts & actual_concepts
        total = pcos_concepts | actual_concepts
        concept_score = len(overlap) / len(total) if total else 0.5
    else:
        concept_score = 0.5

    # Weighted combination: direction is more important
    alignment = direction_score * 0.7 + concept_score * 0.3

    return alignment


def record_outcome(
    question: str,
    pcos_result: dict,
    actual_decision: str,
    category: str = None,
    context: str = None,
):
    """Record the decision and user's actual choice."""
    from runtime.services.outcome_tracker import OutcomeRecord, save_outcome

    # Calculate semantic alignment
    alignment = calculate_decision_alignment(pcos_result, actual_decision)
    match = alignment >= 0.6  # Threshold for "aligned"

    record = OutcomeRecord(
        question=question,
        context=context,
        category=category,
        pcos_recommendation=pcos_result.get("recommendation", ""),
        pcos_confidence=pcos_result.get("confidence", 0),
        pcos_thinking_mode=pcos_result.get("thinking_mode", ""),
        actual_decision=actual_decision,
        decision_match=match,
    )

    outcome_id = save_outcome(record)
    return outcome_id, match, alignment


def interactive_decision():
    """Interactive decision workflow."""
    print("\n" + "=" * 60)
    print("PCOS Decision Workflow")
    print("=" * 60)

    # Step 1: Get question
    print("\n1. 描述你的决策问题:")
    question = input("   问题: ").strip()
    if not question:
        print("   问题不能为空")
        return

    context = input("   背景 (可选): ").strip() or None
    category = input("   类别 (startup/product/tech/business/hiring): ").strip() or None

    # Step 1.5: Ask for original plan (before PCOS)
    print("\n1.5 在问 PCOS 之前，你原本的计划是什么？")
    original_plan = input("   原计划: ").strip()
    if not original_plan:
        original_plan = None

    # Step 2: Ask PCOS
    print("\n2. 正在询问 PCOS...")
    try:
        pcos_result = ask_pcos(question, context)
    except Exception as e:
        print(f"   错误: {e}")
        return

    # Step 3: Show PCOS recommendation
    print("\n3. PCOS 建议:")
    print(f"   思考模式: {pcos_result.get('thinking_mode', 'N/A')}")
    print(f"   建议: {pcos_result.get('recommendation', 'N/A')}")
    print(f"   置信度: {pcos_result.get('confidence', 0):.0%}")

    print("\n   价值观对齐:")
    for v in pcos_result.get("values_alignment", []):
        print(f"   - {v}")

    print("\n   引用信念:")
    for b in pcos_result.get("beliefs_used", []):
        print(f"   - {b}")

    print("\n   风险:")
    for r in pcos_result.get("key_risks", []):
        print(f"   - {r}")

    # Step 4: Get user's decision
    print("\n4. 你的决定:")
    actual_decision = input("   你的选择: ").strip()
    if not actual_decision:
        print("   选择不能为空")
        return

    # Step 4.5: Check if PCOS influenced decision
    influenced = False
    if original_plan:
        # Compare original plan with actual decision
        original_lower = original_plan.lower()
        actual_lower = actual_decision.lower()
        pcos_lower = pcos_result.get("recommendation", "").lower()

        # Extract concepts
        original_concepts = extract_concepts(original_lower)
        actual_concepts = extract_concepts(actual_lower)
        pcos_concepts = extract_concepts(pcos_lower)

        # Check if actual decision moved closer to PCOS recommendation
        original_to_pcos = len(original_concepts & pcos_concepts) / len(pcos_concepts) if pcos_concepts else 0
        actual_to_pcos = len(actual_concepts & pcos_concepts) / len(pcos_concepts) if pcos_concepts else 0

        influenced = actual_to_pcos > original_to_pcos

    # Step 5: Record outcome
    outcome_id, match, alignment = record_outcome(
        question=question,
        pcos_result=pcos_result,
        actual_decision=actual_decision,
        category=category,
        context=context,
    )

    print("\n5. 已记录:")
    print(f"   ID: {outcome_id}")
    print(f"   对齐度: {alignment:.0%}")
    print(f"   与 PCOS 建议{'一致' if match else '不一致'}")
    if original_plan:
        print(f"   PCOS 影响: {'是' if influenced else '否'}")

    # Step 6: Ask for reflection
    print("\n6. 反思 (可选):")
    reflection = input("   为什么做出这个选择? ").strip()
    if reflection:
        from runtime.services.outcome_tracker import update_outcome
        update_outcome(outcome_id, reflection=reflection)
        print("   已记录反思")

    print("\n" + "=" * 60)
    print("决策已记录。未来会用于:")
    print("1. 计算 PCOS 准确率")
    print("2. 计算 Decision Influence Rate")
    print("3. 分析失配案例")
    print("4. 改进 Identity 和 World Model")
    print("=" * 60)


def show_stats():
    """Show current statistics."""
    from runtime.services.outcome_tracker import get_match_rate, list_outcomes

    stats = get_match_rate()
    print("\n" + "=" * 60)
    print("PCOS 统计")
    print("=" * 60)
    print(f"总决策数: {stats['total_decisions']}")
    print(f"与 PCOS 一致: {stats['matches']}")
    print(f"一致率: {stats['match_rate']:.0%}")
    print(f"平均置信度: {stats['avg_confidence']:.0%}" if stats['avg_confidence'] else "")

    outcomes = list_outcomes(5)
    if outcomes:
        print("\n最近 5 个决策:")
        for o in outcomes:
            match = "✓" if o["decision_match"] else "✗"
            print(f"  [{match}] {o['question'][:50]}")

    # Show key metrics summary
    print("\n" + "-" * 60)
    print("关键指标:")
    print("  1. Alignment Rate (对齐率): 一致决策 / 总决策")
    print("  2. Decision Influence Rate (影响率): PCOS 改变决策的比例")
    print("  3. Mismatch Rate (失配率): 不一致决策 / 总决策")
    print("  4. Identity Coverage (Identity 覆盖度): 已验证的价值观比例")
    print("  5. World Model Coverage (信念覆盖度): 已验证的信念比例")


def show_mismatches():
    """Show cases where user didn't follow PCOS."""
    from runtime.services.outcome_tracker import get_mismatch_analysis

    mismatches = get_mismatch_analysis()
    if not mismatches:
        print("\n暂无失配案例")
        return

    print("\n" + "=" * 60)
    print("失配案例 (你的选择 ≠ PCOS 建议)")
    print("=" * 60)

    for m in mismatches:
        print(f"\n问题: {m['question']}")
        print(f"PCOS: {m['pcos_recommendation']}")
        print(f"你: {m['actual_decision']}")
        if m.get("reflection"):
            print(f"反思: {m['reflection']}")
        print("-" * 40)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "stats":
            show_stats()
        elif cmd == "mismatches":
            show_mismatches()
        else:
            print(f"未知命令: {cmd}")
            print("用法: python decision_workflow.py [stats|mismatches]")
    else:
        interactive_decision()
