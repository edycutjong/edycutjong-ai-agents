"""JSON-based usage data storage."""
import json
import os
from agent.calculator import UsageEntry
from config import Config


class UsageStorage:
    """Persistent storage for LLM usage entries."""

    def __init__(self, filepath: str | None = None):
        self.filepath = filepath or Config.STORAGE_FILE
        self._ensure_file()

    def _ensure_file(self):
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump([], f)

    def _load(self) -> list[dict]:
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save(self, data: list[dict]):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def add_entry(self, entry: UsageEntry) -> dict:
        """Add a usage entry."""
        data = self._load()
        data.append(entry.to_dict())
        self._save(data)
        return entry.to_dict()

    def get_all_entries(self) -> list[UsageEntry]:
        """Get all usage entries."""
        return [UsageEntry.from_dict(d) for d in self._load()]

    def get_entries_by_model(self, model: str) -> list[UsageEntry]:
        """Filter entries by model."""
        return [e for e in self.get_all_entries() if e.model == model]

    def get_entries_by_label(self, label: str) -> list[UsageEntry]:
        """Filter entries by label."""
        return [e for e in self.get_all_entries() if e.label == label]

    def clear(self):
        """Clear all entries."""
        self._save([])
