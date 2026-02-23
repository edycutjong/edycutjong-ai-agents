import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class SessionData(BaseModel):
    timestamp: str
    question_type: str
    question: str
    user_answer: str
    score: int
    feedback: str

class ProgressTracker:
    def __init__(self, filename: str = "progress.json"):
        self.filename = filename
        self.sessions: List[SessionData] = []
        self.load_history()

    def load_history(self):
        """Loads progress history from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.sessions = [SessionData(**item) for item in data]
            except (json.JSONDecodeError, ValueError):
                self.sessions = []
        else:
            self.sessions = []

    def save_session(self, question_type: str, question: str, user_answer: str, score: int, feedback: str):
        """Saves a new session to history."""
        session = SessionData(
            timestamp=datetime.now().isoformat(),
            question_type=question_type,
            question=question,
            user_answer=user_answer,
            score=score,
            feedback=feedback
        )
        self.sessions.append(session)
        self._write_to_file()

    def _write_to_file(self):
        """Writes current sessions to JSON file."""
        with open(self.filename, 'w') as f:
            json.dump([session.model_dump() for session in self.sessions], f, indent=4)

    def get_average_score(self, question_type: Optional[str] = None) -> float:
        """Calculates average score, optionally filtered by question type."""
        if not self.sessions:
            return 0.0

        filtered_sessions = self.sessions
        if question_type:
            filtered_sessions = [s for s in self.sessions if s.question_type == question_type]

        if not filtered_sessions:
            return 0.0

        total_score = sum(s.score for s in filtered_sessions)
        return total_score / len(filtered_sessions)

    def get_stats(self) -> Dict[str, float]:
        """Returns stats for all question types."""
        types = set(s.question_type for s in self.sessions)
        stats = {"Overall": self.get_average_score()}
        for t in types:
            stats[t] = self.get_average_score(t)
        return stats
