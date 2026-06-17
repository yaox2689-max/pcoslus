"""Decision Journal

SQLite-based journal for recording decisions with full intermediate state.
Supports future Reflection Engine.
"""

import sqlite3
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path

from ..models import DecideResponse, JournalEntry


# Database path
DB_DIR = Path(__file__).parent.parent / "db"
DB_PATH = DB_DIR / "pcos_v2.db"


def _get_connection() -> sqlite3.Connection:
    """Get SQLite connection."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the database tables."""
    conn = _get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                question TEXT NOT NULL,
                context TEXT,
                context_snapshot TEXT NOT NULL,
                values_used TEXT NOT NULL,
                beliefs_used TEXT NOT NULL,
                thinking_mode TEXT NOT NULL,
                decision TEXT NOT NULL,
                confidence REAL NOT NULL,
                reasoning_chain TEXT NOT NULL,
                key_risks TEXT NOT NULL,
                key_assumptions TEXT NOT NULL,
                options_evaluated TEXT
            )
        """)
        conn.commit()
    finally:
        conn.close()


def save_decision(
    response: DecideResponse,
    context_snapshot: Dict[str, Any],
    values_used: List[str],
    beliefs_used: List[str],
) -> str:
    """Save a decision to the journal with full intermediate state."""
    conn = _get_connection()
    try:
        conn.execute(
            """
            INSERT INTO decisions (
                id, timestamp, question, context, context_snapshot,
                values_used, beliefs_used, thinking_mode, decision,
                confidence, reasoning_chain, key_risks, key_assumptions,
                options_evaluated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                response.decision_id,
                response.timestamp.isoformat(),
                response.question,
                None,  # context from request, not response
                json.dumps(context_snapshot, ensure_ascii=False),
                json.dumps(values_used, ensure_ascii=False),
                json.dumps(beliefs_used, ensure_ascii=False),
                response.thinking_mode.value,
                response.recommendation,
                response.confidence,
                json.dumps(response.reasoning_chain, ensure_ascii=False),
                json.dumps(response.key_risks, ensure_ascii=False),
                json.dumps(response.key_assumptions, ensure_ascii=False),
                json.dumps([opt.model_dump() for opt in response.options_evaluated]),
            ),
        )
        conn.commit()
        return response.decision_id
    finally:
        conn.close()


def get_decision(decision_id: str) -> Optional[JournalEntry]:
    """Get a specific decision by ID."""
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM decisions WHERE id = ?", (decision_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return _row_to_entry(row)
    finally:
        conn.close()


def list_decisions(limit: int = 20) -> List[JournalEntry]:
    """List decisions from the journal."""
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM decisions ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        )
        return [_row_to_entry(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def _row_to_entry(row: sqlite3.Row) -> JournalEntry:
    """Convert a database row to a JournalEntry."""
    return JournalEntry(
        id=row["id"],
        timestamp=datetime.fromisoformat(row["timestamp"]),
        question=row["question"],
        context=row["context"],
        context_snapshot=json.loads(row["context_snapshot"]),
        values_used=json.loads(row["values_used"]),
        beliefs_used=json.loads(row["beliefs_used"]),
        thinking_mode=row["thinking_mode"],
        decision=row["decision"],
        confidence=row["confidence"],
        reasoning_chain=json.loads(row["reasoning_chain"]),
        key_risks=json.loads(row["key_risks"]),
        key_assumptions=json.loads(row["key_assumptions"]),
    )


# Initialize database on import
init_db()
