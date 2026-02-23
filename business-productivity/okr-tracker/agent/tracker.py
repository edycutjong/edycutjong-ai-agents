"""OKR tracker — manage objectives, key results, and track progress."""
from __future__ import annotations
import json, os, uuid
from dataclasses import dataclass, field
from datetime import datetime
from config import Config

@dataclass
class KeyResult:
    id: str = ""
    title: str = ""
    target: float = 100
    current: float = 0
    unit: str = "%"
    def __post_init__(self):
        if not self.id: self.id = uuid.uuid4().hex[:8]
    @property
    def progress(self) -> float:
        return min(round(self.current / self.target * 100, 1) if self.target else 0, 100)
    @property
    def status(self) -> str:
        if self.progress >= 100: return "completed"
        if self.progress >= 70: return "on-track"
        if self.progress >= 30: return "at-risk"
        return "behind"
    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "target": self.target, "current": self.current, "unit": self.unit, "progress": self.progress, "status": self.status}

@dataclass
class Objective:
    id: str = ""
    title: str = ""
    owner: str = ""
    quarter: str = ""
    key_results: list[KeyResult] = field(default_factory=list)
    created_at: str = ""
    def __post_init__(self):
        if not self.id: self.id = uuid.uuid4().hex[:8]
        if not self.created_at: self.created_at = datetime.now().isoformat()
    @property
    def progress(self) -> float:
        if not self.key_results: return 0
        return round(sum(kr.progress for kr in self.key_results) / len(self.key_results), 1)
    @property
    def status(self) -> str:
        p = self.progress
        if p >= 100: return "completed"
        if p >= 70: return "on-track"
        if p >= 30: return "at-risk"
        return "behind"
    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "owner": self.owner, "quarter": self.quarter,
                "key_results": [kr.to_dict() for kr in self.key_results], "progress": self.progress, "status": self.status}

class OKRStore:
    def __init__(self, filepath: str | None = None):
        self.filepath = filepath or Config.STORAGE_FILE
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath) or ".", exist_ok=True)
            with open(self.filepath, "w") as f: json.dump([], f)
    def _load(self) -> list[dict]:
        try:
            with open(self.filepath) as f: return json.load(f)
        except: return []
    def _save(self, data: list[dict]):
        with open(self.filepath, "w") as f: json.dump(data, f, indent=2)
    def add_objective(self, obj: Objective) -> str:
        data = self._load(); data.append(obj.to_dict()); self._save(data); return obj.id
    def get_all(self) -> list[dict]:
        return self._load()
    def update_key_result(self, obj_id: str, kr_id: str, current: float) -> bool:
        data = self._load()
        for obj in data:
            if obj["id"] == obj_id:
                for kr in obj.get("key_results", []):
                    if kr["id"] == kr_id:
                        kr["current"] = current
                        kr["progress"] = min(round(current / kr["target"] * 100, 1) if kr["target"] else 0, 100)
                        kr["status"] = "completed" if kr["progress"] >= 100 else "on-track" if kr["progress"] >= 70 else "at-risk" if kr["progress"] >= 30 else "behind"
                        self._save(data); return True
        return False

def get_summary(objectives: list[dict]) -> dict:
    total = len(objectives)
    if total == 0: return {"total": 0, "avg_progress": 0}
    statuses = {"completed": 0, "on-track": 0, "at-risk": 0, "behind": 0}
    total_progress = 0
    for o in objectives:
        s = o.get("status", "behind"); statuses[s] = statuses.get(s, 0) + 1
        total_progress += o.get("progress", 0)
    return {"total": total, "avg_progress": round(total_progress / total, 1), **statuses}

def format_okrs_markdown(objectives: list[dict]) -> str:
    summary = get_summary(objectives)
    lines = ["# OKR Dashboard", f"**Objectives:** {summary['total']} | **Avg Progress:** {summary['avg_progress']}%", ""]
    emoji_map = {"completed": "✅", "on-track": "🟢", "at-risk": "🟡", "behind": "🔴"}
    for o in objectives:
        e = emoji_map.get(o.get("status", ""), "⬜")
        lines.append(f"## {e} {o['title']} ({o.get('progress', 0)}%)")
        if o.get("owner"): lines.append(f"**Owner:** {o['owner']} | **Quarter:** {o.get('quarter', 'N/A')}")
        for kr in o.get("key_results", []):
            ke = emoji_map.get(kr.get("status", ""), "⬜")
            bar = "█" * int(kr.get("progress", 0) / 10) + "░" * (10 - int(kr.get("progress", 0) / 10))
            lines.append(f"- {ke} {kr['title']}: {kr.get('current', 0)}/{kr.get('target', 0)} {kr.get('unit', '')} [{bar}]")
        lines.append("")
    return "\n".join(lines)
