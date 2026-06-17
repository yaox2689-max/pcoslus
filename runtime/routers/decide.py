"""Decision API Router

Endpoints for making and querying decisions.
"""

import json
import re
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from ..models import (
    DecideRequest,
    DecideResponse,
    JournalEntry,
    EvaluatedOption,
    OptionScore,
    ThinkingMode,
    SimulateRequest,
    SimulateResponse,
    RuntimeTrace,
    ValueConflicts,
    CounterArgument,
)
from ..services.context_builder import build_full_context, extract_topics
from ..services.prompt_builder import build_system_prompt, build_user_prompt
from ..services.claude_client import get_llm_client
from ..services.decision_journal import save_decision, get_decision, list_decisions
from ..services.trace_logger import save_trace


router = APIRouter(prefix="/decide", tags=["decisions"])


def _parse_json_response(text: str) -> dict:
    """Parse JSON from Claude response."""
    # Try parsing the entire response as JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find JSON block in markdown code block
    json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to find any JSON-like object
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse JSON from response")


def _build_decide_response(data: dict, question: str) -> DecideResponse:
    """Build DecideResponse from parsed JSON."""
    # Parse options
    options = []
    for opt in data.get("options_evaluated", []):
        try:
            score_data = opt.get("score", {})
            score = OptionScore(
                value_alignment=float(score_data.get("value_alignment", 0.5)),
                belief_support=float(score_data.get("belief_support", 0.5)),
                resource_feasibility=float(score_data.get("resource_feasibility", 0.5)),
                risk_acceptability=float(score_data.get("risk_acceptability", 0.5)),
                learning_potential=float(score_data.get("learning_potential", 0.5)),
                weighted_total=float(score_data.get("weighted_total", 0.5)),
            )
            options.append(EvaluatedOption(option=opt.get("option", ""), score=score))
        except Exception:
            continue

    # Parse value conflicts
    vc_data = data.get("value_conflicts", {})
    value_conflicts = ValueConflicts(
        gains=vc_data.get("gains", []),
        losses=vc_data.get("losses", []),
        net_alignment=float(vc_data.get("net_alignment", 0.5)),
        severity=float(vc_data.get("severity", 0.5)),
        dominant_conflict=vc_data.get("dominant_conflict"),
    )

    # Parse counter argument
    ca_data = data.get("counter_argument", {})
    counter_argument = None
    if ca_data:
        counter_argument = CounterArgument(
            position=ca_data.get("position", ""),
            reasoning=ca_data.get("reasoning", ""),
        )

    return DecideResponse(
        question=question,
        thinking_mode=ThinkingMode(data.get("thinking_mode", "slow")),
        thinking_mode_reason=data.get("thinking_mode_reason", ""),
        recommendation=data.get("recommendation", ""),
        confidence=float(data.get("confidence", 0.5)),
        reasoning_chain=data.get("reasoning_chain", []),
        options_evaluated=options,
        value_conflicts=value_conflicts,
        counter_argument=counter_argument,
        key_risks=data.get("key_risks", []),
        key_assumptions=data.get("key_assumptions", []),
        values_alignment=data.get("values_alignment", []),
        beliefs_used=data.get("beliefs_used", []),
    )


@router.post("/", response_model=DecideResponse)
async def make_decision(request: DecideRequest) -> DecideResponse:
    """Make a PCOS decision."""

    print("\n" + "=" * 60)
    print("PCOS Decision Request")
    print("=" * 60)
    print(f"Question: {request.question}")
    if request.context:
        print(f"Context: {request.context[:100]}...")

    # Build context (with topic filtering)
    context_data = build_full_context(request.question, request.context)

    topics = context_data.get("topics", [])
    beliefs_count = len(context_data["world_model"]["relevant_beliefs"])
    values_count = len(context_data["identity"]["core_values"])

    print(f"\n[Context Builder]")
    print(f"  Topics detected: {', '.join(topics)}")
    print(f"  Beliefs loaded: {beliefs_count}")
    print(f"  Values loaded: {values_count}")
    print(f"  Coverage: {context_data['world_model']['coverage_score']:.0%}")

    # Build prompts
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(
        question=request.question,
        context=request.context or "",
        options=request.options,
        identity=context_data["identity"],
        world_model=context_data["world_model"],
    )

    print(f"\n[LLM Request]")
    print(f"  Provider: {get_llm_client().provider}")
    print(f"  Model: {get_llm_client().model}")
    print(f"  Prompt length: {len(user_prompt)} chars")

    # Call Claude
    client = get_llm_client()
    response_text = client.reason(system_prompt, user_prompt)

    print(f"\n[LLM Response]")
    print(f"  Response length: {len(response_text)} chars")

    # Parse JSON response
    try:
        data = _parse_json_response(response_text)
        decision = _build_decide_response(data, request.question)
    except Exception as e:
        print(f"\n[ERROR] Failed to parse response: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse Claude response: {str(e)}"
        )

    # Extract values and beliefs used
    values_used = decision.values_alignment
    beliefs_used = decision.beliefs_used

    print(f"\n[Decision Result]")
    print(f"  Thinking mode: {decision.thinking_mode.value}")
    print(f"  Confidence: {decision.confidence:.0%}")
    print(f"  Recommendation: {decision.recommendation[:100]}...")
    print(f"  Options evaluated: {len(decision.options_evaluated)}")
    print(f"  Values aligned: {len(values_used)}")
    print(f"  Beliefs used: {len(beliefs_used)}")
    print("=" * 60 + "\n")

    # Save to journal with intermediate state
    save_decision(
        decision,
        context_snapshot=context_data,
        values_used=values_used,
        beliefs_used=beliefs_used,
    )

    # Save trace
    trace = RuntimeTrace(
        question=request.question,
        context=request.context,
        topics_detected=context_data.get("topics", []),
        context_snapshot=context_data,
        values_used=values_used,
        beliefs_used=beliefs_used,
        thinking_mode=decision.thinking_mode.value,
        decision=decision.recommendation,
        confidence=decision.confidence,
    )
    save_trace(trace)

    return decision


@router.post("/simulate", response_model=SimulateResponse)
async def simulate_option(request: SimulateRequest) -> SimulateResponse:
    """Simulate a specific option without making a full decision."""

    # Build context
    context_data = build_full_context(request.question, request.context)

    # Build simulation prompt
    system_prompt = """You are PCOS, a decision-making engine.
Analyze a specific option for a decision.

Respond with JSON:
{
  "alignment": 0.0 to 1.0,
  "conflicts": ["value that conflicts"],
  "risks": ["risk 1", "risk 2"],
  "assumptions": ["assumption 1"],
  "recommendation": "brief assessment"
}"""

    values_str = ", ".join(context_data["identity"]["core_values"])
    beliefs = context_data["world_model"]["relevant_beliefs"]
    beliefs_str = "\n".join([f"- {b.get('content', '')}" for b in beliefs])

    user_prompt = f"""## Context
Values: {values_str}
Beliefs:
{beliefs_str}

## Decision
{request.question}

## Option to Simulate
{request.option}

Context: {request.context or 'N/A'}

Respond with JSON only."""

    # Call Claude
    client = get_llm_client()
    response_text = client.reason(system_prompt, user_prompt)

    # Parse response
    try:
        data = _parse_json_response(response_text)
        return SimulateResponse(
            option=request.option,
            alignment=float(data.get("alignment", 0.5)),
            conflicts=data.get("conflicts", []),
            risks=data.get("risks", []),
            assumptions=data.get("assumptions", []),
            recommendation=data.get("recommendation", ""),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse Claude response: {str(e)}"
        )


@router.get("/journal", response_model=List[JournalEntry])
async def get_journal(limit: int = 20) -> List[JournalEntry]:
    """Get decision journal entries."""
    return list_decisions(limit=limit)


@router.get("/journal/{decision_id}", response_model=JournalEntry)
async def get_journal_entry(decision_id: str) -> JournalEntry:
    """Get a specific decision journal entry."""
    entry = get_decision(decision_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Decision not found")
    return entry


@router.get("/traces")
async def get_traces(limit: int = 20):
    """List recent runtime traces."""
    from ..services.trace_logger import list_traces
    return list_traces(limit=limit)


@router.get("/providers")
async def list_providers():
    """List available LLM providers."""
    from ..services.claude_client import PROVIDERS
    import os
    return {
        "current": os.getenv("LLM_PROVIDER", "deepseek"),
        "available": list(PROVIDERS.keys()),
    }


@router.post("/providers/{provider}")
async def switch_provider(provider: str):
    """Switch LLM provider at runtime."""
    from ..services.claude_client import get_llm_client, PROVIDERS

    if provider not in PROVIDERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown provider: {provider}. Must be one of: {list(PROVIDERS.keys())}"
        )

    try:
        client = get_llm_client(provider)
        return {
            "status": "switched",
            "provider": client.provider,
            "model": client.model,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
