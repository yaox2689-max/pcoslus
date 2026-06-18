"""Outcome Engine v2

Records decision outcomes with decision quality tracking.
This is the most valuable data PCOS will ever collect.

Key insight: Outcome != Decision Quality
- Good outcome can be luck (bad decision, good result)
- Bad outcome can be bad luck (good decision, bad result)
- We need to track both separately
"""

import sqlite3
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path
from pydantic import BaseModel, Field


# Database path
DB_DIR = Path(__file__).parent.parent / "db"
DB_PATH = DB_DIR / "pcos_outcomes.db"


# ─────────────────────────────────────────────────────────────
# Data Models
# ─────────────────────────────────────────────────────────────

class Prediction(BaseModel):
    """Predictions made at decision time."""
    expected_salary: Optional[str] = None      # "increase" | "stable" | "decrease"
    expected_growth: Optional[str] = None      # "high" | "medium" | "low"
    expected_risk: Optional[str] = None        # "high" | "medium" | "low"
    expected_learning: Optional[str] = None    # "high" | "medium" | "low"
    expected_network: Optional[str] = None     # "expand" | "stable" | "shrink"
    custom: Dict[str, str] = Field(default_factory=dict)


class ActualResult(BaseModel):
    """Actual results recorded later."""
    salary: Optional[str] = None
    growth: Optional[str] = None
    risk: Optional[str] = None
    learning: Optional[str] = None
    network: Optional[str] = None
    custom: Dict[str, str] = Field(default_factory=dict)


class OutcomeRecord(BaseModel):
    """A decision outcome record with quality tracking."""
    id: str = Field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    decision_id: str = Field(description="ID of the original decision")
    question: str
    decision: str = Field(description="What was decided")
    decision_date: datetime = Field(default_factory=datetime.now)

    # Prediction (recorded at decision time)
    prediction: Optional[Prediction] = None

    # Expected outcome (recorded at decision time)
    expected_outcome: Optional[str] = None

    # Actual outcome (recorded later: 7d, 30d, 90d)
    actual_outcome: Optional[str] = None
    actual_result: Optional[ActualResult] = None
    outcome_score: Optional[int] = Field(None, ge=1, le=5, description="1=worst, 5=best")
    outcome_date: Optional[datetime] = None

    # Decision quality (separate from outcome!)
    decision_quality: Optional[str] = Field(None, description="good | neutral | bad - was the decision good AT THE TIME?")
    quality_reasoning: Optional[str] = Field(None, description="Why was the decision good/bad?")
    controllability: Optional[str] = Field(None, description="high | medium | low - how much was in our control?")

    # Learning
    lesson: Optional[str] = Field(None, description="What did we learn?")
    surprise: Optional[str] = Field(None, description="expected | better_than_expected | worse_than_expected")

    # Identity update candidates (NEVER auto-update, always human review)
    identity_update_candidates: List[Dict[str, Any]] = Field(default_factory=list)

    # Reflection queue
    reflection_status: str = Field(default="pending", description="pending | queued | reviewed")
    reflection_trigger: Optional[str] = Field(None, description="What triggered reflection need")

    # Metadata
    backfill_date: Optional[datetime] = Field(None, description="When was outcome recorded")
    status: str = Field(default="pending", description="pending | filled | expired")


class PendingOutcome(BaseModel):
    """A decision waiting for outcome."""
    outcome_id: str
    decision_id: str
    question: str
    decision: str
    decision_date: str
    days_since: int
    reminder_due: bool
    prediction: Optional[Prediction] = None


# ─────────────────────────────────────────────────────────────
# Database
# ─────────────────────────────────────────────────────────────

def _get_connection() -> sqlite3.Connection:
    """Get SQLite connection."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_outcome_db() -> None:
    """Initialize the outcomes database."""
    conn = _get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS decision_outcomes (
                id TEXT PRIMARY KEY,
                decision_id TEXT NOT NULL,
                question TEXT NOT NULL,
                decision TEXT NOT NULL,
                decision_date TEXT NOT NULL,

                prediction TEXT,
                expected_outcome TEXT,

                actual_outcome TEXT,
                actual_result TEXT,
                outcome_score INTEGER,
                outcome_date TEXT,

                decision_quality TEXT,
                quality_reasoning TEXT,
                controllability TEXT,

                lesson TEXT,
                surprise TEXT,

                identity_update_candidates TEXT,

                reflection_status TEXT DEFAULT 'pending',
                reflection_trigger TEXT,

                backfill_date TEXT,
                status TEXT DEFAULT 'pending',

                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Indexes
        conn.execute("CREATE INDEX IF NOT EXISTS idx_outcomes_status ON decision_outcomes(status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_outcomes_decision_id ON decision_outcomes(decision_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_outcomes_reflection ON decision_outcomes(reflection_status)")

        conn.commit()
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────
# CRUD Operations
# ─────────────────────────────────────────────────────────────

def create_outcome(
    decision_id: str,
    question: str,
    decision: str,
    expected_outcome: str = None,
    prediction: Prediction = None,
    decision_date: datetime = None,
) -> str:
    """Create a new outcome record (at decision time)."""
    now = datetime.now()
    outcome_id = now.strftime("%Y%m%d_%H%M%S")

    conn = _get_connection()
    try:
        conn.execute(
            """
            INSERT INTO decision_outcomes (
                id, decision_id, question, decision, decision_date,
                prediction, expected_outcome, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                outcome_id,
                decision_id,
                question,
                decision,
                (decision_date or now).isoformat(),
                json.dumps(prediction.model_dump() if prediction else {}, ensure_ascii=False),
                expected_outcome,
                "pending",
                now.isoformat(),
                now.isoformat(),
            ),
        )
        conn.commit()
        return outcome_id
    finally:
        conn.close()


def record_outcome(
    outcome_id: str,
    actual_outcome: str,
    outcome_score: int,
    actual_result: ActualResult = None,
    decision_quality: str = None,
    quality_reasoning: str = None,
    controllability: str = None,
    lesson: str = None,
    surprise: str = None,
    identity_update_candidates: List[Dict] = None,
    reflection_trigger: str = None,
) -> bool:
    """Record the actual outcome (backfill later)."""
    now = datetime.now()

    conn = _get_connection()
    try:
        conn.execute(
            """
            UPDATE decision_outcomes SET
                actual_outcome = ?,
                actual_result = ?,
                outcome_score = ?,
                outcome_date = ?,
                decision_quality = ?,
                quality_reasoning = ?,
                controllability = ?,
                lesson = ?,
                surprise = ?,
                identity_update_candidates = ?,
                reflection_status = ?,
                reflection_trigger = ?,
                backfill_date = ?,
                status = 'filled',
                updated_at = ?
            WHERE id = ?
            """,
            (
                actual_outcome,
                json.dumps(actual_result.model_dump() if actual_result else {}, ensure_ascii=False),
                outcome_score,
                now.isoformat(),
                decision_quality,
                quality_reasoning,
                controllability,
                lesson,
                surprise,
                json.dumps(identity_update_candidates or [], ensure_ascii=False),
                "queued" if identity_update_candidates else "pending",
                reflection_trigger,
                now.isoformat(),
                now.isoformat(),
                outcome_id,
            ),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def get_outcome(outcome_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific outcome."""
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM decision_outcomes WHERE id = ?", (outcome_id,)
        )
        row = cursor.fetchone()
        if row:
            d = dict(row)
            # Parse JSON fields
            for field in ["prediction", "actual_result", "identity_update_candidates"]:
                if d.get(field):
                    try:
                        d[field] = json.loads(d[field])
                    except:
                        pass
            return d
        return None
    finally:
        conn.close()


def get_pending_outcomes() -> List[PendingOutcome]:
    """Get all decisions waiting for outcome."""
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM decision_outcomes WHERE status = 'pending' ORDER BY decision_date ASC"
        )
        results = []
        now = datetime.now()
        for row in cursor.fetchall():
            d = dict(row)
            decision_date = datetime.fromisoformat(d["decision_date"])
            days_since = (now - decision_date).days

            prediction = None
            if d.get("prediction"):
                try:
                    prediction = Prediction(**json.loads(d["prediction"]))
                except:
                    pass

            results.append(PendingOutcome(
                outcome_id=d["id"],
                decision_id=d["decision_id"],
                question=d["question"],
                decision=d["decision"],
                decision_date=d["decision_date"],
                days_since=days_since,
                reminder_due=days_since >= 7,
                prediction=prediction,
            ))
        return results
    finally:
        conn.close()


def get_filled_outcomes(limit: int = 50) -> List[Dict[str, Any]]:
    """Get all filled outcomes (for Reflection Engine)."""
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM decision_outcomes WHERE status = 'filled' ORDER BY outcome_date DESC LIMIT ?",
            (limit,),
        )
        results = []
        for row in cursor.fetchall():
            d = dict(row)
            for field in ["prediction", "actual_result", "identity_update_candidates"]:
                if d.get(field):
                    try:
                        d[field] = json.loads(d[field])
                    except:
                        pass
            results.append(d)
        return results
    finally:
        conn.close()


def get_reflection_queue() -> List[Dict[str, Any]]:
    """Get outcomes queued for reflection (have identity_update_candidates)."""
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM decision_outcomes WHERE reflection_status = 'queued' ORDER BY outcome_date DESC"
        )
        results = []
        for row in cursor.fetchall():
            d = dict(row)
            for field in ["prediction", "actual_result", "identity_update_candidates"]:
                if d.get(field):
                    try:
                        d[field] = json.loads(d[field])
                    except:
                        pass
            results.append(d)
        return results
    finally:
        conn.close()


def get_outcome_stats() -> Dict[str, Any]:
    """Get outcome statistics."""
    conn = _get_connection()
    try:
        cursor = conn.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'filled' THEN 1 ELSE 0 END) as filled,
                AVG(CASE WHEN status = 'filled' THEN outcome_score END) as avg_outcome_score,
                SUM(CASE WHEN decision_quality = 'good' THEN 1 ELSE 0 END) as good_decisions,
                SUM(CASE WHEN decision_quality = 'bad' THEN 1 ELSE 0 END) as bad_decisions,
                SUM(CASE WHEN reflection_status = 'queued' THEN 1 ELSE 0 END) as pending_reflections
            FROM decision_outcomes
        """)
        row = cursor.fetchone()
        return {
            "total": row["total"],
            "pending": row["pending"],
            "filled": row["filled"],
            "avg_outcome_score": round(row["avg_outcome_score"], 2) if row["avg_outcome_score"] else None,
            "good_decisions": row["good_decisions"],
            "bad_decisions": row["bad_decisions"],
            "pending_reflections": row["pending_reflections"],
        }
    finally:
        conn.close()


# Initialize on import
init_outcome_db()
