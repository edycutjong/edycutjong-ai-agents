import json
import os
import uuid
from datetime import datetime
try:
    from config import Config
except ImportError:  # pragma: no cover
    from ..config import Config  # pragma: no cover

class IssueTracker:
    def __init__(self, data_path=Config.DATA_PATH):
        self.data_path = data_path
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:  # pragma: no cover
                self.issues = json.load(f)  # pragma: no cover
        else:
            self.issues = []

    def _save_data(self):
        with open(self.data_path, "w") as f:
            json.dump(self.issues, f, indent=2)

    def get_all_issues(self):
        return self.issues

    def get_issue(self, issue_id):
        for issue in self.issues:
            if issue["id"] == issue_id:
                return issue
        return None  # pragma: no cover

    def add_issue(self, title, description, team=None):
        issue_id = f"ISSUE-{len(self.issues) + 101}"
        new_issue = {
            "id": issue_id,
            "title": title,
            "description": description,
            "status": Config.STATUS_OPEN,
            "severity": "medium",  # Default, to be updated by AI
            "team": team or "Unassigned",
            "created_at": datetime.now().isoformat(),
            "labels": [],
            "analysis": "",
            "sentiment": "neutral"
        }
        self.issues.append(new_issue)
        self._save_data()
        return new_issue

    def update_issue(self, issue_id, updates):
        for issue in self.issues:
            if issue["id"] == issue_id:
                issue.update(updates)
                self._save_data()
                return issue
        return None  # pragma: no cover

    def delete_issue(self, issue_id):
        self.issues = [i for i in self.issues if i["id"] != issue_id]  # pragma: no cover
        self._save_data()  # pragma: no cover
