"""Outcome Engine

Records decision outcomes and feeds the Learning/Reflection loop.
This is the most valuable data PCOS will ever collect.
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

class OutcomeRecord(BaseModel):
    """A decision outcome record."""
    id: str = Field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    decision_id: str = Field(description="ID of the original decision")
    question: str
    decision: str = Field(description="What was decided")
    decision_date: datetime = Field(default_factory=datetime.now)

    # Expected outcome (recorded at decision time)
    expected_outcome: Optional[str] = None

    # Actual outcome (recorded later: 7d, 30d, 90d)
    actual_outcome: Optional[str] = None
    outcome_score: Optional[int] = Field(None, ge=1, le=5, description="1=worst, 5=best")
    outcome_date: Optional[datetime] = None

    # Learning
    lesson: Optional[str] = Field(None, description="What did we learn?")
    surprise: Optional[str] = Field(None, description="expected | better_than_expected | worse_than_expected")

    # Identity update candidates
    identity_update_candidates: List[Dict[str, Any]] = Field(default_factory=list)

    # Metadata
    backfill_date: Optional[datetime] = Field(None, description="When was outcome recorded")
    status: str = Field(default="pending", description="pending | filled | expired")


class PendingOutcome(BaseModel):
    """A decision waiting for outcome."""
    decision_id: str
    question: str
    decision: str
    decision_date: str
    days_since: int
    reminder_due: bool


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

                expected_outcome TEXT,
                actual_outcome TEXT,
                outcome_score INTEGER,
                outcome_date TEXT,

                lesson TEXT,
                surprise TEXT,

                identity_update_candidates TEXT,

                backfill_date TEXT,
                status TEXT DEFAULT 'pending',

                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Index for fast lookups
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_outcomes_status
            ON decision_outcomes(status)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_outcomes_decision_id
            ON decision_outcomes(decision_id)
        """)

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
                expected_outcome, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                outcome_id,
                decision_id,
                question,
                decision,
                (decision_date or now).isoformat(),
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
    lesson: str = None,
    surprise: str = None,
    identity_update_candidates: List[Dict] = None,
) -> bool:
    """Record the actual outcome (backfill later)."""
    now = datetime.now()

    conn = _get_connection()
    try:
        conn.execute(
            """
            UPDATE decision_outcomes SET
                actual_outcome = ?,
                outcome_score = ?,
                outcome_date = ?,
                lesson = ?,
                surprise = ?,
                identity_update_candidates = ?,
                backfill_date = ?,
                status = 'filled',
                updated_at = ?
            WHERE id = ?
            """,
            (
                actual_outcome,
                outcome_score,
                now.isoformat(),
                lesson,
                surprise,
                json.dumps(identity_update_candidates or [], ensure_ascii=False),
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
        return dict(row) if row else None
    finally:
        conn.close()


def get_pending_outcomes() -> List[PendingOutcome]:
    """Get all decisions waiting for outcome."""
    conn = _get_connection()
    try:
        cursor = conn.execute(
            """
            SELECT * FROM decision_outcomes
            WHERE status = 'pending'
            ORDER BY decision_date ASC
            """
        )
        results = []
        now = datetime.now()
        for row in cursor.fetchall():
            d = dict(row)
            decision_date = datetime.fromisoformat(d["decision_date"])
            days_since = (now - decision_date).days
            results.append(PendingOutcome(
                decision_id=d["decision_id"],
                question=d["question"],
                decision=d["decision"],
                decision_date=d["decision_date"],
                days_since=days_since,
                reminder_due=days_since >= 7,
            ))
        return results
    finally:
        conn.close()


def get_filled_outcomes(limit: int = 50) -> List[Dict[str, Any]]:
    """Get all filled outcomes (for Reflection Engine)."""
    conn = _get_connection()
    try:
        cursor = conn.execute(
            """
            SELECT * FROM decision_outcomes
            WHERE status = 'filled'
            ORDER BY outcome_date DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]
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
                AVG(CASE WHEN status = 'filled' THEN outcome_score END) as avg_score
            FROM decision_outcomes
        """)
        row = cursor.fetchone()
        return {
            "total": row["total"],
            "pending": row["pending"],
            "filled": row["filled"],
            "avg_score": round(row["avg_score"], 2) if row["avg_score"] else None,
        }
    finally:
        conn.close()


# Initialize on import
init_outcome_db()
