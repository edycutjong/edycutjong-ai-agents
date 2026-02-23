import json
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import config

MOOD_TRACKER_FILE = config.MOOD_TRACKER_FILE
JOURNAL_FILE = config.JOURNAL_FILE

class MoodEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    mood: str
    energy: int = Field(..., ge=1, le=10)
    context: Optional[str] = None

class JournalEntry(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    prompt: str
    response: str
    mood_entry: Optional[MoodEntry] = None
    tags: List[str] = []

class Tracker:
    def __init__(self):
        self.mood_file = MOOD_TRACKER_FILE
        self.journal_file = JOURNAL_FILE
        self._ensure_files()

    def _ensure_files(self):
        if not self.mood_file.exists():
            self.mood_file.write_text("[]")
        if not self.journal_file.exists():
            self.journal_file.write_text("[]")

    def add_mood(self, mood: str, energy: int, context: Optional[str] = None) -> MoodEntry:
        entry = MoodEntry(mood=mood, energy=energy, context=context)
        history = self.get_mood_history()
        history.append(entry)
        self._save_mood_history(history)
        return entry

    def get_mood_history(self) -> List[MoodEntry]:
        try:
            data = json.loads(self.mood_file.read_text())
            return [MoodEntry(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_mood_history(self, history: List[MoodEntry]):
        data = [json.loads(entry.model_dump_json()) for entry in history]
        self.mood_file.write_text(json.dumps(data, indent=2))

    def save_journal_entry(self, entry: JournalEntry):
        entries = self.get_journal_entries()
        entries.append(entry)
        data = [json.loads(e.model_dump_json()) for e in entries]
        self.journal_file.write_text(json.dumps(data, indent=2))

    def get_journal_entries(self) -> List[JournalEntry]:
        try:
            data = json.loads(self.journal_file.read_text())
            return [JournalEntry(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
