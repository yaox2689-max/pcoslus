"""Decision Outcome Tracker

Records real decisions and their outcomes for Learning Engine.
"""

import sqlite3
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field


# Database path
DB_DIR = Path(__file__).parent / "db"
DB_PATH = DB_DIR / "pcos_outcomes.db"


class OutcomeRecord(BaseModel):
    """A decision outcome record."""
    id: str = Field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    timestamp: datetime = Field(default_factory=datetime.now)

    # Decision context
    question: str
    context: Optional[str] = None
    category: Optional[str] = None  # startup, product, tech, business, hiring

    # PCOS recommendation
    pcos_recommendation: str
    pcos_confidence: float
    pcos_thinking_mode: str

    # User's actual decision
    actual_decision: str
    decision_match: bool  # Did user follow PCOS recommendation?

    # Outcomes (filled later)
    outcome_after_7_days: Optional[str] = None  # positive, negative, neutral, pending
    outcome_after_30_days: Optional[str] = None
    outcome_after_90_days: Optional[str] = None
    outcome_notes: Optional[str] = None

    # Reflection
    reflection: Optional[str] = None
    identity_update_needed: bool = False
    world_model_update_needed: bool = False


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
            CREATE TABLE IF NOT EXISTS outcomes (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                question TEXT NOT NULL,
                context TEXT,
                category TEXT,
                pcos_recommendation TEXT NOT NULL,
                pcos_confidence REAL NOT NULL,
                pcos_thinking_mode TEXT NOT NULL,
                actual_decision TEXT NOT NULL,
                decision_match BOOLEAN NOT NULL,
                outcome_after_7_days TEXT,
                outcome_after_30_days TEXT,
                outcome_after_90_days TEXT,
                outcome_notes TEXT,
                reflection TEXT,
                identity_update_needed BOOLEAN DEFAULT FALSE,
                world_model_update_needed BOOLEAN DEFAULT FALSE
            )
        """)
        conn.commit()
    finally:
        conn.close()


def save_outcome(record: OutcomeRecord) -> str:
    """Save an outcome record."""
    conn = _get_connection()
    try:
        conn.execute(
            """
            INSERT INTO outcomes (
                id, timestamp, question, context, category,
                pcos_recommendation, pcos_confidence, pcos_thinking_mode,
                actual_decision, decision_match,
                outcome_after_7_days, outcome_after_30_days, outcome_after_90_days,
                outcome_notes, reflection,
                identity_update_needed, world_model_update_needed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.timestamp.isoformat(),
                record.question,
                record.context,
                record.category,
                record.pcos_recommendation,
                record.pcos_confidence,
                record.pcos_thinking_mode,
                record.actual_decision,
                record.decision_match,
                record.outcome_after_7_days,
                record.outcome_after_30_days,
                record.outcome_after_90_days,
                record.outcome_notes,
                record.reflection,
                record.identity_update_needed,
                record.world_model_update_needed,
            ),
        )
        conn.commit()
        return record.id
    finally:
        conn.close()


def get_outcome(outcome_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific outcome by ID."""
    conn = _get_connection()
    try:
        cursor = conn.execute("SELECT * FROM outcomes WHERE id = ?", (outcome_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def list_outcomes(limit: int = 50) -> List[Dict[str, Any]]:
    """List outcomes."""
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM outcomes ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def update_outcome(
    outcome_id: str,
    outcome_after_7_days: str = None,
    outcome_after_30_days: str = None,
    outcome_after_90_days: str = None,
    outcome_notes: str = None,
    reflection: str = None,
) -> bool:
    """Update an outcome record."""
    conn = _get_connection()
    try:
        updates = []
        params = []

        if outcome_after_7_days:
            updates.append("outcome_after_7_days = ?")
            params.append(outcome_after_7_days)
        if outcome_after_30_days:
            updates.append("outcome_after_30_days = ?")
            params.append(outcome_after_30_days)
        if outcome_after_90_days:
            updates.append("outcome_after_90_days = ?")
            params.append(outcome_after_90_days)
        if outcome_notes:
            updates.append("outcome_notes = ?")
            params.append(outcome_notes)
        if reflection:
            updates.append("reflection = ?")
            params.append(reflection)

        if not updates:
            return False

        params.append(outcome_id)
        sql = f"UPDATE outcomes SET {', '.join(updates)} WHERE id = ?"
        conn.execute(sql, params)
        conn.commit()
        return True
    finally:
        conn.close()


def get_match_rate() -> Dict[str, Any]:
    """Get decision match rate statistics."""
    conn = _get_connection()
    try:
        cursor = conn.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN decision_match THEN 1 ELSE 0 END) as matches,
                AVG(pcos_confidence) as avg_confidence
            FROM outcomes
        """)
        row = cursor.fetchone()
        total = row["total"]
        matches = row["matches"]
        return {
            "total_decisions": total,
            "matches": matches,
            "match_rate": matches / total if total > 0 else 0,
            "avg_confidence": row["avg_confidence"],
        }
    finally:
        conn.close()


def get_mismatch_analysis() -> List[Dict[str, Any]]:
    """Get cases where user didn't follow PCOS recommendation."""
    conn = _get_connection()
    try:
        cursor = conn.execute("""
            SELECT * FROM outcomes
            WHERE decision_match = FALSE
            ORDER BY timestamp DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


# Initialize on import
init_outcome_db()
