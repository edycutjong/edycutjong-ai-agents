import json
import os
import uuid
from datetime import datetime
from config import Config

class MeetingStorage:
    def __init__(self, filepath=None):
        self.filepath = filepath or Config.STORAGE_FILE
        self._ensure_file()

    def _ensure_file(self):
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def _load(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save(self, data):
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def save_meeting(self, transcript, summary, action_items, email_draft):
        meetings = self._load()
        meeting_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        meeting = {
            "id": meeting_id,
            "timestamp": timestamp,
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items,
            "email_draft": email_draft
        }

        meetings.append(meeting)
        self._save(meetings)
        return meeting_id

    def get_all_meetings(self):
        # Sort by timestamp descending
        meetings = self._load()
        return sorted(meetings, key=lambda x: x['timestamp'], reverse=True)

    def get_meeting(self, meeting_id):
        meetings = self._load()
        for m in meetings:
            if m["id"] == meeting_id:
                return m
        return None

    def search_meetings(self, query):
        meetings = self._load()
        results = []
        query = query.lower()
        for m in meetings:
            if (query in m.get("transcript", "").lower() or
                query in m.get("summary", "").lower() or
                any(query in item.get("task", "").lower() for item in m.get("action_items", []))):
                results.append(m)
        return sorted(results, key=lambda x: x['timestamp'], reverse=True)
