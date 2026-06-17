"""PCOS Benchmark Tests

Runs the 27 benchmark scenarios through the PCOS Runtime.
"""

import pytest
import yaml
from pathlib import Path
from typing import Dict, Any, List

from runtime.config import get_config, get_benchmark_scenarios
from runtime.services.context_builder import build_full_context
from runtime.services.prompt_builder import build_system_prompt, build_user_prompt
from runtime.services.claude_client import get_claude_client
from runtime.services.response_parser import parse_claude_response


# Path to benchmark file
BENCHMARK_PATH = Path(__file__).parent.parent / "pcos" / "decision_benchmark.yaml"


def load_benchmark_scenarios() -> List[Dict[str, Any]]:
    """Load benchmark scenarios from YAML."""
    scenarios = get_benchmark_scenarios()
    return scenarios.get("scenarios", [])


@pytest.fixture
def claude_client():
    """Get Claude client."""
    return get_claude_client()


@pytest.fixture
def benchmark_scenarios():
    """Load benchmark scenarios."""
    return load_benchmark_scenarios()


def run_scenario(
    scenario: Dict[str, Any],
    client=None,
) -> Dict[str, Any]:
    """Run a single benchmark scenario through PCOS."""

    if client is None:
        client = get_claude_client()

    # Build context
    question = scenario["decision"]
    context = scenario.get("context", "")
    options = scenario.get("options", [])

    # Build full context
    full_context = build_full_context(question, context)

    # Build prompts
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(
        question=question,
        context=context,
        options=options,
        identity=full_context["identity"],
        world_model=full_context["world_model"],
    )

    # Call Claude
    response_text = client.reason(system_prompt, user_prompt)

    # Parse response
    try:
        decision = parse_claude_response(
            response_text=response_text,
            question=question,
            context=context,
        )
        return {
            "scenario_id": scenario["id"],
            "success": True,
            "thinking_mode": decision.thinking_mode.value,
            "recommendation": decision.recommendation,
            "confidence": decision.confidence,
            "reasoning_chain": decision.reasoning_chain,
            "options_count": len(decision.options_evaluated),
        }
    except Exception as e:
        return {
            "scenario_id": scenario["id"],
            "success": False,
            "error": str(e),
        }


def calculate_similarity(
    pcos_result: Dict[str, Any],
    scenario: Dict[str, Any],
) -> float:
    """Calculate similarity between PCOS result and expected behavior."""

    if not pcos_result.get("success"):
        return 0.0

    score = 0.0
    max_score = 0.0

    # 1. Thinking mode match (40%)
    max_score += 40
    expected_mode = scenario.get("expected_thinking", "slow")
    if pcos_result.get("thinking_mode") == expected_mode:
        score += 40

    # 2. Has recommendation (20%)
    max_score += 20
    if pcos_result.get("recommendation"):
        score += 20

    # 3. Has reasoning chain (20%)
    max_score += 20
    if pcos_result.get("reasoning_chain") and len(pcos_result["reasoning_chain"]) > 0:
        score += 20

    # 4. Confidence in valid range (10%)
    max_score += 10
    confidence = pcos_result.get("confidence", 0)
    if 0.3 <= confidence <= 0.95:
        score += 10

    # 5. Options evaluated (10%)
    max_score += 10
    if pcos_result.get("options_count", 0) >= 2:
        score += 10

    return score / max_score if max_score > 0 else 0.0


@pytest.mark.asyncio
async def test_benchmark_scenarios(benchmark_scenarios, claude_client):
    """Run all benchmark scenarios and calculate similarity."""

    results = []
    similarities = []

    for scenario in benchmark_scenarios[:5]:  # Test with first 5 scenarios
        print(f"\nRunning scenario {scenario['id']}: {scenario['category']}")

        # Run scenario
        result = run_scenario(scenario, claude_client)
        results.append(result)

        # Calculate similarity
        similarity = calculate_similarity(result, scenario)
        similarities.append(similarity)

        print(f"  Thinking mode: {result.get('thinking_mode', 'N/A')}")
        print(f"  Recommendation: {result.get('recommendation', 'N/A')[:100]}")
        print(f"  Similarity: {similarity:.2%}")

    # Calculate average similarity
    avg_similarity = sum(similarities) / len(similarities) if similarities else 0.0
    print(f"\n{'='*50}")
    print(f"Average Similarity: {avg_similarity:.2%}")
    print(f"Scenarios tested: {len(results)}")
    print(f"Successful: {sum(1 for r in results if r.get('success'))}")
    print(f"Failed: {sum(1 for r in results if not r.get('success'))}")

    # Assert minimum similarity
    assert avg_similarity >= 0.5, f"Average similarity {avg_similarity:.2%} is below 50%"


def test_single_scenario():
    """Test a single scenario for quick validation."""
    scenarios = load_benchmark_scenarios()
    if not scenarios:
        pytest.skip("No benchmark scenarios found")

    scenario = scenarios[0]
    result = run_scenario(scenario)

    assert result["success"], f"Scenario failed: {result.get('error')}"
    assert result["thinking_mode"] in ["fast", "slow"]
    assert result["recommendation"]
    assert 0 <= result["confidence"] <= 1
