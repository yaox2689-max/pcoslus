"""PCOS Identity Experiment

Test whether Identity actually influences decisions.
Compare: Test A (opposite identity) vs Test B (real identity)
"""

import requests
import json
import time


BASE_URL = "http://localhost:8001"


def ask_pcos(question: str, context: str = None) -> dict:
    """Ask PCOS via API."""
    payload = {"question": question}
    if context:
        payload["context"] = context
    response = requests.post(f"{BASE_URL}/decide/", json=payload, timeout=120)
    return response.json()


def run_experiment():
    """Run the Identity experiment.

    Method: Compare PCOS output with two different contexts that
    emphasize different values, to see if Identity influences output.
    """
    test_cases = [
        {
            "question": "Should I learn AI or Java?",
            "context_a": "You value job security and stability above all. You prefer proven technologies. You are risk-averse.",
            "context_b": "You value innovation and creativity. You prefer cutting-edge technologies. You are risk-seeking.",
        },
        {
            "question": "Should I pivot from consulting to product?",
            "context_a": "You have only 2 months runway. You cannot afford any revenue disruption. Stability is your top priority.",
            "context_b": "You have 12 months runway. You can afford to experiment. Long-term growth matters more than short-term revenue.",
        },
        {
            "question": "Should I accept VC funding?",
            "context_a": "You highly value autonomy and control. You prefer bootstrapping. You don't want external interference.",
            "context_b": "You highly value rapid growth. You're comfortable giving up control for resources. Speed is your priority.",
        },
    ]

    print("\n" + "=" * 60)
    print("PCOS Identity Experiment")
    print("=" * 60)
    print("\nMethod: Same question, different value contexts")
    print("If Identity matters, recommendations should differ.")
    print("\nTest A: Conservative values (security, stability)")
    print("Test B: Aggressive values (innovation, growth)")

    results = []

    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {i}: {test['question']}")
        print(f"{'='*60}")

        # Test A: Conservative values
        print("\n[Test A: Conservative Values]")
        try:
            result_a = ask_pcos(test["question"], test["context_a"])
            rec_a = result_a.get("recommendation", "ERROR")
            conf_a = result_a.get("confidence", 0)
            print(f"  Recommendation: {rec_a[:100]}")
            print(f"  Confidence: {conf_a:.0%}")
        except Exception as e:
            print(f"  Error: {e}")
            rec_a = "ERROR"
            conf_a = 0
            result_a = {}

        time.sleep(2)  # Rate limit

        # Test B: Aggressive values
        print("\n[Test B: Aggressive Values]")
        try:
            result_b = ask_pcos(test["question"], test["context_b"])
            rec_b = result_b.get("recommendation", "ERROR")
            conf_b = result_b.get("confidence", 0)
            print(f"  Recommendation: {rec_b[:100]}")
            print(f"  Confidence: {conf_b:.0%}")
        except Exception as e:
            print(f"  Error: {e}")
            rec_b = "ERROR"
            conf_b = 0
            result_b = {}

        # Compare
        print("\n[Comparison]")

        # Check if recommendations are different
        from decision_workflow import extract_concepts
        concepts_a = extract_concepts(rec_a.lower())
        concepts_b = extract_concepts(rec_b.lower())

        if concepts_a and concepts_b:
            overlap = concepts_a & concepts_b
            total = concepts_a | concepts_b
            similarity = len(overlap) / len(total) if total else 0
        else:
            similarity = 0.5

        conf_diff = abs(conf_a - conf_b)

        print(f"  Recommendation Similarity: {similarity:.0%}")
        print(f"  Confidence Difference: {conf_diff:.0%}")

        # Analyze value conflicts
        vc_a = result_a.get("value_conflicts", {})
        vc_b = result_b.get("value_conflicts", {})

        if vc_a and vc_b:
            print(f"\n  Test A Value Conflicts:")
            print(f"    Gains: {vc_a.get('gains', [])}")
            print(f"    Losses: {vc_a.get('losses', [])}")

            print(f"\n  Test B Value Conflicts:")
            print(f"    Gains: {vc_b.get('gains', [])}")
            print(f"    Losses: {vc_b.get('losses', [])}")

        # Check counter arguments
        ca_a = result_a.get("counter_argument", {})
        ca_b = result_b.get("counter_argument", {})

        if ca_a and ca_b:
            print(f"\n  Test A Counter: {ca_a.get('position', 'N/A')[:80]}")
            print(f"  Test B Counter: {ca_b.get('position', 'N/A')[:80]}")

        # Determine influence
        if similarity < 0.6:
            print("\n  [OK] Identity STRONGLY influenced decision")
            print("     Different value contexts -> different recommendations")
        elif similarity < 0.8:
            print("\n  [WARN] Identity MODERATELY influenced decision")
            print("     Some variation detected")
        else:
            print("\n  [FAIL] Identity did NOT influence decision")
            print("     Similar recommendations despite different values")

        results.append({
            "test": test["question"],
            "similarity": similarity,
            "conf_diff": conf_diff,
            "influenced": similarity < 0.7,
        })

    # Summary
    print("\n" + "=" * 60)
    print("EXPERIMENT SUMMARY")
    print("=" * 60)

    influenced_count = sum(1 for r in results if r["influenced"])
    avg_similarity = sum(r["similarity"] for r in results) / len(results) if results else 0
    avg_conf_diff = sum(r["conf_diff"] for r in results) / len(results) if results else 0

    print(f"\nTests run: {len(results)}")
    print(f"Identity influenced: {influenced_count}/{len(results)}")
    print(f"Average recommendation similarity: {avg_similarity:.0%}")
    print(f"Average confidence difference: {avg_conf_diff:.0%}")

    print("\n" + "-" * 60)
    print("INTERPRETATION:")
    print("-" * 60)

    if avg_similarity > 0.85:
        print("\n[FAIL] CONCLUSION: Identity does NOT influence decisions")
        print("   PCOS is likely just Prompt Engineering with context.")
        print("   The same question with different values gets the same answer.")
        print("\n   NEXT STEP: Strengthen Identity rules in Decision Engine")
    elif avg_similarity > 0.65:
        print("\n[WARN] CONCLUSION: Identity has LIMITED influence")
        print("   Some variation, but recommendations are mostly similar.")
        print("   Identity is partially working.")
        print("\n   NEXT STEP: Improve how Identity affects reasoning")
    else:
        print("\n[OK] CONCLUSION: Identity DOES influence decisions!")
        print("   Different value contexts produce different recommendations.")
        print("   PCOS has demonstrated identity-conditioned reasoning.")
        print("\n   NEXT STEP: Continue collecting real decisions to validate")

    return results


if __name__ == "__main__":
    run_experiment()
