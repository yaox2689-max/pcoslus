"""Runtime Trace Logger

Records execution traces for debugging and future learning.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from ..models import RuntimeTrace


# Trace directory
TRACE_DIR = Path(__file__).parent.parent / "traces"


def _ensure_trace_dir():
    """Ensure trace directory exists."""
    TRACE_DIR.mkdir(parents=True, exist_ok=True)


def save_trace(trace: RuntimeTrace) -> str:
    """Save a runtime trace to file."""
    _ensure_trace_dir()

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"trace_{timestamp}.json"
    filepath = TRACE_DIR / filename

    # Save trace
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(trace.model_dump(), f, ensure_ascii=False, indent=2, default=str)

    return str(filepath)


def list_traces(limit: int = 20) -> List[Dict[str, Any]]:
    """List recent traces."""
    _ensure_trace_dir()

    traces = []
    for filepath in sorted(TRACE_DIR.glob("trace_*.json"), reverse=True)[:limit]:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                trace_data = json.load(f)
                traces.append({
                    "file": filepath.name,
                    "timestamp": trace_data.get("timestamp"),
                    "question": trace_data.get("question", "")[:100],
                    "decision": trace_data.get("decision", "")[:100],
                })
        except Exception:
            continue

    return traces


def get_trace(filename: str) -> Dict[str, Any]:
    """Get a specific trace by filename."""
    filepath = TRACE_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Trace not found: {filename}")

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
