import json
from pathlib import Path
from typing import Any

from tools.logging_tool import log_event

MEMORY_FILE = Path("data/memory/memory.json")
MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_memory() -> list[dict]:
    if not MEMORY_FILE.exists():
        return []
    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        log_event("storage", "Failed to decode memory.json, resetting.", {})
        return []

def save_memory(entries: list[dict]) -> None:
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with MEMORY_FILE.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

def append_memory(entry: dict[str, Any]) -> None:
    entries = load_memory()
    entries.append(entry)
    save_memory(entries)
    log_event("storage", "Appended memory entry", entry)
