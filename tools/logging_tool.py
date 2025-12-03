import datetime
import json
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def log_event(component: str, message: str, payload: dict | None = None) -> None:
    """Simple JSONL logger for observability."""
    LOG_DIR.mkdir(exist_ok=True)
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "component": component,
        "message": message,
        "payload": payload or {},
    }
    log_file = LOG_DIR / "events.jsonl"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
