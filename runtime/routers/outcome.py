"""Outcome API Router v2

Endpoints for recording and querying decision outcomes.
Now with decision quality tracking and prediction support.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from ..services.outcome_engine import (
    create_outcome,
    record_outcome,
    get_outcome,
    get_pending_outcomes,
    get_filled_outcomes,
    get_reflection_queue,
    get_outcome_stats,
    PendingOutcome,
    Prediction,
    ActualResult,
)


router = APIRouter(prefix="/outcome", tags=["outcomes"])


# ─────────────────────────────────────────────────────────────
# Request Models
# ─────────────────────────────────────────────────────────────

class CreateOutcomeRequest(BaseModel):
    """Create outcome at decision time."""
    decision_id: str
    question: str
    decision: str
    expected_outcome: Optional[str] = None
    prediction: Optional[Prediction] = None


class RecordOutcomeRequest(BaseModel):
    """Record actual outcome (backfill)."""
    actual_outcome: str
    outcome_score: int = Field(ge=1, le=5)
    actual_result: Optional[ActualResult] = None
    decision_quality: Optional[str] = Field(None, description="good | neutral | bad")
    quality_reasoning: Optional[str] = None
    controllability: Optional[str] = Field(None, description="high | medium | low")
    lesson: Optional[str] = None
    surprise: Optional[str] = Field(None, description="expected | better_than_expected | worse_than_expected")
    identity_update_candidates: Optional[List[Dict[str, Any]]] = None
    reflection_trigger: Optional[str] = None


# ─────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────

@router.post("/")
async def create_outcome_endpoint(req: CreateOutcomeRequest):
    """Create outcome record at decision time."""
    outcome_id = create_outcome(
        decision_id=req.decision_id,
        question=req.question,
        decision=req.decision,
        expected_outcome=req.expected_outcome,
        prediction=req.prediction,
    )
    return {"outcome_id": outcome_id, "status": "pending"}


@router.put("/{outcome_id}")
async def record_outcome_endpoint(outcome_id: str, req: RecordOutcomeRequest):
    """Record actual outcome (backfill)."""
    existing = get_outcome(outcome_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Outcome not found")

    success = record_outcome(
        outcome_id=outcome_id,
        actual_outcome=req.actual_outcome,
        outcome_score=req.outcome_score,
        actual_result=req.actual_result,
        decision_quality=req.decision_quality,
        quality_reasoning=req.quality_reasoning,
        controllability=req.controllability,
        lesson=req.lesson,
        surprise=req.surprise,
        identity_update_candidates=req.identity_update_candidates,
        reflection_trigger=req.reflection_trigger,
    )
    return {"status": "filled", "outcome_id": outcome_id}


@router.get("/pending")
async def get_pending_endpoint() -> List[PendingOutcome]:
    """Get all decisions waiting for outcome."""
    return get_pending_outcomes()


@router.get("/filled")
async def get_filled_endpoint(limit: int = 50):
    """Get filled outcomes."""
    return get_filled_outcomes(limit=limit)


@router.get("/reflection-queue")
async def get_reflection_queue_endpoint():
    """Get outcomes queued for reflection (have identity_update_candidates)."""
    return get_reflection_queue()


@router.get("/stats")
async def get_stats_endpoint():
    """Get outcome statistics."""
    return get_outcome_stats()


@router.get("/{outcome_id}")
async def get_outcome_endpoint(outcome_id: str):
    """Get a specific outcome."""
    outcome = get_outcome(outcome_id)
    if not outcome:
        raise HTTPException(status_code=404, detail="Outcome not found")
    return outcome
