import logging
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class MemoryEntry:
    action: str
    result: object


class Memory:
    """Simple in-memory store for agent context and completed steps."""

    def __init__(self, max_entries: int = 100) -> None:
        self._entries: List[MemoryEntry] = []
        self.completed_steps: List[str] = []
        self._max_entries = max_entries

    def store(self, action: str, result: object) -> None:
        if len(self._entries) >= self._max_entries:
            self._entries.pop(0)
        self._entries.append(MemoryEntry(action=action, result=result))

    def recall(self, limit: int = 5) -> List[MemoryEntry]:
        return self._entries[-limit:]

    def mark_completed(self, step: str) -> None:
        if step not in self.completed_steps:
            self.completed_steps.append(step)
