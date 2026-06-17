"""Prompt Builder

Builds structured prompts for Claude reasoning.
Enforces JSON output format with counter-arguments and value conflicts.
"""

from typing import Dict, Any, List, Optional
from ..config import get_config


SYSTEM_PROMPT = """You are PCOS (Personal Cognitive Operating System), a decision-making engine.

Your job: help the user make decisions that align with their values and beliefs.

CRITICAL RULES:
1. NEVER say "all values align" - every decision has tradeoffs
2. ALWAYS identify which values GAIN and which values LOSE
3. ALWAYS provide the STRONGEST counter-argument
4. BELIEFS must be used for REASONING, not just repeated
5. SCORES must reflect REAL tradeoffs, not rubber-stamp approval
6. Consider user's DECISION PATTERNS (e.g., prefer_optionality, avoid_binary_choices)

DECISION PATTERNS TO CONSIDER:
- prefer_optionality: User prefers options that preserve more choices
- avoid_binary_choices: User looks for combination strategies, not either/or
- hedge_uncertainty: User hedges risks when uncertain
- long_term_compounding: User prefers long-term gains over short-term
- risk_managed_growth: User takes risks but needs safety nets

You MUST respond with valid JSON only. No markdown, no explanation outside the JSON.

Required JSON format:
{
  "thinking_mode": "fast" or "slow",
  "thinking_mode_reason": "why this mode was selected",
  "recommendation": "your recommendation in one sentence",
  "confidence": 0.0 to 1.0,
  "reasoning_chain": ["reason 1 - must use beliefs to derive conclusion", ...],
  "options_evaluated": [
    {
      "option": "option text",
      "score": {
        "value_alignment": 0.0 to 1.0,
        "belief_support": 0.0 to 1.0,
        "resource_feasibility": 0.0 to 1.0,
        "risk_acceptability": 0.0 to 1.0,
        "learning_potential": 0.0 to 1.0,
        "weighted_total": 0.0 to 1.0
      }
    }
  ],
  "value_conflicts": {
    "gains": ["value that is strengthened by this decision"],
    "losses": ["value that is weakened by this decision"],
    "net_alignment": 0.0 to 1.0,
    "severity": 0.0 to 1.0,
    "dominant_conflict": "e.g., autonomy_vs_security"
  },
  "counter_argument": {
    "position": "the strongest argument AGAINST the recommendation",
    "reasoning": "why someone might reasonably disagree"
  },
  "key_risks": ["risk 1", "risk 2", ...],
  "key_assumptions": ["assumption 1", "assumption 2", ...],
  "beliefs_used": ["belief 1 - how it was used in reasoning", ...]
}

Evaluation criteria weights:
- value_alignment: 0.30
- belief_support: 0.25
- resource_feasibility: 0.20
- risk_acceptability: 0.15
- learning_potential: 0.10

REASONING CHAIN RULES:
- Do NOT just repeat beliefs
- DO: "Belief X + Value Y + Constraint Z → Conclusion"
- Example: "AI market growing (belief) + user values learning (value) + 12-month horizon (constraint) → AI has higher compound return than Java"

VALUE CONFLICT RULES:
- Every decision strengthens some values and weakens others
- Example: "Learning AI gains: creativity, learning. Loses: career_security (if AI hype fades)"
- net_alignment = (gains_weight - losses_weight) / total_values

COUNTER-ARGUMENT RULES:
- Must be the STRONGEST reasonable argument against your recommendation
- Not a straw man - something a smart person would actually argue
- Example: "Java still powers 90% of enterprise systems. AI skills may be overvalued in short-term job market."

THINKING MODE:
- Fast: simple, low risk, familiar pattern
- Slow: complex, high risk, novel situation"""


def build_system_prompt() -> str:
    """Build the system prompt for PCOS reasoning."""
    return SYSTEM_PROMPT


def build_user_prompt(
    question: str,
    context: str,
    options: Optional[List[str]],
    identity: Dict[str, Any],
    world_model: Dict[str, Any],
) -> str:
    """Build the user prompt with filtered context."""

    # Format identity (only relevant parts)
    values = identity["core_values"]
    values_str = ", ".join(values)
    focus = identity["current_focus"]
    focus_str = f"{focus.get('primary', 'N/A')}/{focus.get('secondary', 'N/A')}"

    # Format beliefs (only relevant ones)
    beliefs = world_model["relevant_beliefs"]
    beliefs_str = "\n".join([
        f"- {b.get('content', 'N/A')} (confidence: {b.get('confidence', 0.5)})"
        for b in beliefs
    ]) if beliefs else "- No relevant beliefs found"

    # Format contradictions
    contradictions = world_model.get("contradictions", [])
    contradictions_str = "\n".join([
        f"- {c.get('description', 'N/A')}"
        for c in contradictions
    ]) if contradictions else "- None"

    # Format decision patterns from identity
    decision_patterns = identity.get("decision_patterns", [])
    patterns_str = ""
    if decision_patterns:
        patterns_str = "\n".join([
            f"- {p.get('name', 'N/A')}: {p.get('description', 'N/A')} (confidence: {p.get('confidence', 0.5)})"
            for p in decision_patterns
        ])
    else:
        patterns_str = "- No decision patterns recorded yet"

    # Build prompt
    prompt = f"""## User Context

Core Values: {values_str}
Focus: {focus_str}
Model Coverage: {world_model.get('coverage_score', 0.5):.0%}

IMPORTANT: Each value has weight based on user's actual behavior, not self-reporting.

## User's Decision Patterns

{patterns_str}

IMPORTANT: Consider these patterns when making recommendations. For example:
- If user has "prefer_optionality", recommend options that preserve more choices
- If user has "avoid_binary_choices", look for combination strategies
- If user has "hedge_uncertainty", suggest hedging when risk is high

## Relevant Beliefs

{beliefs_str}

## Known Contradictions

{contradictions_str}

## Decision

Question: {question}"""

    if context:
        prompt += f"\nContext: {context}"

    if options:
        prompt += "\n\nOptions:\n" + "\n".join([f"- {opt}" for opt in options])

    prompt += """

## Instructions

1. Assess the decision complexity and select thinking mode
2. Consider user's DECISION PATTERNS (e.g., prefer_optionality)
3. For each option, score using the 5 criteria
4. For the recommended option, identify:
   - Which values GAIN from this decision
   - Which values LOSE from this decision
   - The SEVERITY of the conflict (0-1)
   - The DOMINANT CONFLICT (e.g., autonomy_vs_security)
   - The STRONGEST counter-argument
5. In reasoning_chain, show HOW you used beliefs to reach conclusions (not just repeat them)
6. If user has "prefer_optionality" pattern, consider combination strategies, not just binary choices

Respond with JSON only."""

    return prompt
