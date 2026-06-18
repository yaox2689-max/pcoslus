"""Reflection API Router

Endpoints for reflection analysis and candidate management.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

from ..services.reflection_engine import (
    generate_reflection_report,
    get_pending_candidates,
    approve_candidate,
    reject_candidate,
)


router = APIRouter(prefix="/reflection", tags=["reflection"])


class CandidateAction(BaseModel):
    """Action on a candidate."""
    name: str
    reason: str = None


@router.get("/report")
async def get_reflection_report():
    """Generate a complete reflection report."""
    report = generate_reflection_report()
    return {
        "generated_at": report.generated_at,
        "total_outcomes": report.total_outcomes,
        "filled_outcomes": report.filled_outcomes,
        "pattern_candidates": [
            {
                "name": p.name,
                "description": p.description,
                "evidence_count": p.evidence_count,
                "success_rate": p.success_rate,
                "confidence": p.confidence,
                "status": p.status,
            }
            for p in report.pattern_candidates
        ],
        "value_insights": [
            {
                "value_name": v.value_name,
                "times_aligned": v.times_aligned,
                "avg_outcome_when_aligned": v.avg_outcome_when_aligned,
                "insight": v.insight,
            }
            for v in report.value_insights
        ],
        "top_lessons": report.top_lessons,
        "identity_update_candidates": report.identity_update_candidates,
    }


@router.get("/candidates")
async def get_candidates():
    """Get identity update candidates pending review."""
    return get_pending_candidates()


@router.post("/candidates/approve")
async def approve_candidate_endpoint(req: CandidateAction):
    """Approve an identity update candidate."""
    success = approve_candidate(req.name)
    return {"status": "approved", "name": req.name}


@router.post("/candidates/reject")
async def reject_candidate_endpoint(req: CandidateAction):
    """Reject an identity update candidate."""
    success = reject_candidate(req.name, req.reason)
    return {"status": "rejected", "name": req.name}
