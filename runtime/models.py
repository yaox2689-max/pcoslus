"""PCOS Pydantic Models

Defines request/response models and internal data structures.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


# ─────────────────────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────────────────────

class ThinkingMode(str, Enum):
    FAST = "fast"
    SLOW = "slow"


# ─────────────────────────────────────────────────────────────
# Score Models
# ─────────────────────────────────────────────────────────────

class OptionScore(BaseModel):
    """Score for a single option across evaluation criteria."""
    value_alignment: float = Field(ge=0, le=1)
    belief_support: float = Field(ge=0, le=1)
    resource_feasibility: float = Field(ge=0, le=1)
    risk_acceptability: float = Field(ge=0, le=1)
    learning_potential: float = Field(ge=0, le=1)
    weighted_total: float = Field(ge=0, le=1)


class EvaluatedOption(BaseModel):
    """An option with its evaluation scores."""
    option: str
    score: OptionScore


# ─────────────────────────────────────────────────────────────
# Request Models
# ─────────────────────────────────────────────────────────────

class DecideRequest(BaseModel):
    """Request for /decide endpoint."""
    question: str = Field(..., description="The decision question")
    context: Optional[str] = Field(None, description="Additional context")
    options: Optional[List[str]] = Field(None, description="Pre-defined options (optional)")


class SimulateRequest(BaseModel):
    """Request for /simulate endpoint."""
    question: str = Field(..., description="The decision question")
    option: str = Field(..., description="The option to simulate")
    context: Optional[str] = Field(None, description="Additional context")


# ─────────────────────────────────────────────────────────────
# Response Models
# ─────────────────────────────────────────────────────────────

class ValueConflicts(BaseModel):
    """Value conflicts for a decision."""
    gains: List[str] = Field(default_factory=list, description="Values strengthened")
    losses: List[str] = Field(default_factory=list, description="Values weakened")
    net_alignment: float = Field(ge=0, le=1, default=0.5)
    severity: float = Field(ge=0, le=1, default=0.5, description="How severe the conflict is (0=minor, 1=severe)")
    dominant_conflict: Optional[str] = Field(None, description="The primary value conflict, e.g., 'autonomy_vs_security'")


class CounterArgument(BaseModel):
    """Strongest argument against the recommendation."""
    position: str = Field(description="The counter-argument position")
    reasoning: str = Field(description="Why someone might disagree")


class DecisionDirection(str, Enum):
    """Direction of a decision."""
    POSITIVE = "positive"  # accepting, doing, moving forward
    NEGATIVE = "negative"  # rejecting, avoiding, not doing
    NEUTRAL = "neutral"    # balanced, hedging, combination


class DecideResponse(BaseModel):
    """Response from /decide endpoint."""
    decision_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    question: str
    thinking_mode: ThinkingMode
    thinking_mode_reason: str
    recommendation: str
    confidence: float = Field(ge=0, le=1)
    reasoning_chain: List[str]
    options_evaluated: List[EvaluatedOption]
    value_conflicts: ValueConflicts = Field(default_factory=ValueConflicts)
    counter_argument: Optional[CounterArgument] = None
    key_risks: List[str]
    key_assumptions: List[str]
    values_alignment: List[str]
    beliefs_used: List[str]


class SimulateResponse(BaseModel):
    """Response from /simulate endpoint."""
    option: str
    alignment: float = Field(ge=0, le=1, description="Value alignment score")
    conflicts: List[str] = Field(description="Values that conflict with this option")
    risks: List[str] = Field(description="Key risks for this option")
    assumptions: List[str] = Field(description="Key assumptions")
    recommendation: str = Field(description="Overall assessment")


class JournalEntry(BaseModel):
    """A decision journal entry with full intermediate state."""
    id: str
    timestamp: datetime
    question: str
    context: Optional[str]
    context_snapshot: Dict[str, Any] = Field(description="Full context at decision time")
    values_used: List[str] = Field(description="Values that influenced the decision")
    beliefs_used: List[str] = Field(description="Beliefs that influenced the decision")
    thinking_mode: str
    decision: str = Field(description="The recommendation/decision")
    confidence: float
    reasoning_chain: List[str]
    key_risks: List[str]
    key_assumptions: List[str]


# ─────────────────────────────────────────────────────────────
# Internal Models
# ─────────────────────────────────────────────────────────────

class IdentityContext(BaseModel):
    """Loaded identity context for a decision."""
    core_values: List[str]
    current_focus: Dict[str, Any]
    preferences: Dict[str, Any]


class WorldModelContext(BaseModel):
    """Loaded world model context for a decision."""
    relevant_beliefs: List[Dict[str, Any]]
    contradictions: List[Dict[str, Any]]
    blind_spots: List[str]
    coverage_score: float = Field(ge=0, le=1)


class RuntimeTrace(BaseModel):
    """Trace of runtime execution for debugging."""
    question: str
    context: Optional[str]
    topics_detected: List[str]
    context_snapshot: Dict[str, Any]
    values_used: List[str]
    beliefs_used: List[str]
    thinking_mode: str
    decision: str
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.now)
