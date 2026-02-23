"""Standup report generation engine."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from collections import defaultdict
from config import Config


@dataclass
class StandupEntry:
    """A single standup report entry."""
    id: str = ""
    date: str = ""
    author: str = ""
    yesterday: list[str] = field(default_factory=list)
    today: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    mood: str = ""  # 🟢 Good, 🟡 Okay, 🔴 Bad

    def __post_init__(self):
        if not self.id:
            self.id = datetime.now().strftime("%Y%m%d%H%M%S")
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "StandupEntry":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class StandupStorage:
    """JSON-backed storage for standup reports."""

    def __init__(self, filepath: str | None = None):
        self.filepath = filepath or Config.STORAGE_FILE
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath) or ".", exist_ok=True)
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

    def add(self, entry: StandupEntry) -> str:
        data = self._load()
        data.append(entry.to_dict())
        self._save(data)
        return entry.id

    def get_all(self) -> list[StandupEntry]:
        return [StandupEntry.from_dict(d) for d in self._load()]

    def get_by_date(self, date: str) -> list[StandupEntry]:
        return [e for e in self.get_all() if e.date == date]

    def get_by_author(self, author: str) -> list[StandupEntry]:
        return [e for e in self.get_all() if e.author.lower() == author.lower()]

    def get_last_n_days(self, days: int) -> list[StandupEntry]:
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return [e for e in self.get_all() if e.date >= cutoff]

    def clear(self):
        self._save([])


def generate_daily_report(entries: list[StandupEntry], date: str | None = None) -> str:
    """Generate a team daily standup report."""
    date = date or datetime.now().strftime("%Y-%m-%d")
    day_entries = [e for e in entries if e.date == date] if entries else []

    lines = [
        f"# Daily Standup — {date}",
        f"**Team Size:** {len(day_entries)} member(s)",
        "",
    ]

    if not day_entries:
        lines.append("*No standup reports submitted.*")
        return "\n".join(lines)

    for entry in day_entries:
        mood = f" {entry.mood}" if entry.mood else ""
        lines.append(f"## {entry.author}{mood}")

        if entry.yesterday:
            lines.append("**Yesterday:**")
            for item in entry.yesterday:
                lines.append(f"- {item}")

        if entry.today:
            lines.append("**Today:**")
            for item in entry.today:
                lines.append(f"- {item}")

        if entry.blockers:
            lines.append("**🚫 Blockers:**")
            for item in entry.blockers:
                lines.append(f"- ⚠️ {item}")

        if entry.tags:
            lines.append(f"**Tags:** {', '.join(f'`{t}`' for t in entry.tags)}")

        lines.append("")

    # Summary
    all_blockers = [b for e in day_entries for b in e.blockers]
    if all_blockers:
        lines.append("## ⚠️ Active Blockers")
        for b in all_blockers:
            lines.append(f"- {b}")
        lines.append("")

    return "\n".join(lines)


def generate_weekly_summary(entries: list[StandupEntry]) -> str:
    """Generate a weekly summary from multiple days of standups."""
    by_author = defaultdict(lambda: {"items": [], "blockers": [], "days": 0})

    for entry in entries:
        a = by_author[entry.author]
        a["items"].extend(entry.today)
        a["items"].extend(entry.yesterday)
        a["blockers"].extend(entry.blockers)
        a["days"] += 1

    lines = [
        "# Weekly Standup Summary",
        f"**Reports:** {len(entries)} entries from {len(by_author)} team member(s)",
        "",
    ]

    for author, data in sorted(by_author.items()):
        lines.append(f"## {author} ({data['days']} days)")
        unique_items = list(dict.fromkeys(data["items"]))
        for item in unique_items[:10]:
            lines.append(f"- {item}")
        if data["blockers"]:
            lines.append(f"**Blockers:** {len(data['blockers'])}")
        lines.append("")

    return "\n".join(lines)


def generate_blocker_report(entries: list[StandupEntry]) -> str:
    """Generate a focused blocker report."""
    blockers_by_author = defaultdict(list)
    for entry in entries:
        for b in entry.blockers:
            blockers_by_author[entry.author].append({"blocker": b, "date": entry.date})

    if not blockers_by_author:
        return "# Blocker Report\n\n✅ No active blockers!"

    lines = ["# Blocker Report", ""]
    total = sum(len(v) for v in blockers_by_author.values())
    lines.append(f"**{total} blocker(s)** across {len(blockers_by_author)} team member(s)\n")

    for author, items in sorted(blockers_by_author.items()):
        lines.append(f"## {author}")
        for item in items:
            lines.append(f"- [{item['date']}] {item['blocker']}")
        lines.append("")

    return "\n".join(lines)
