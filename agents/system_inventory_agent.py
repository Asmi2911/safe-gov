from typing import Dict, Any
from tools.logging_tool import log_event

class SystemInventoryAgent:
    """Describes the audited system (mocked for this project)."""

    def __init__(self, system_config: Dict[str, Any] | None = None):
        self.system_config = system_config or {
            "model": "mock-llm",
            "endpoint": "local-mock",
            "use_cases": ["demo", "safety-audit"],
            "max_tokens": 256,
        }

    def run(self) -> Dict[str, Any]:
        log_event("SystemInventoryAgent", "Loaded system inventory", self.system_config)
        return self.system_config
