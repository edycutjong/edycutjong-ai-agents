"""Webhook request storage and management."""
from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from config import Config


@dataclass
class WebhookRequest:
    """A captured webhook request."""
    id: str = ""
    method: str = "POST"
    path: str = "/"
    headers: dict = field(default_factory=dict)
    body: str = ""
    query_params: dict = field(default_factory=dict)
    timestamp: str = ""
    source_ip: str = ""
    content_type: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "WebhookRequest":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def summary(self) -> str:
        """One-line summary of the request."""
        body_preview = (self.body[:50] + "...") if len(self.body) > 50 else self.body
        return f"[{self.id}] {self.method} {self.path} ({self.content_type}) — {body_preview}"


class WebhookStorage:
    """JSON-backed storage for captured webhook requests."""

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

    def add(self, request: WebhookRequest) -> str:
        """Store a webhook request. Returns the request ID."""
        data = self._load()
        data.append(request.to_dict())
        self._save(data)
        return request.id

    def get_all(self) -> list[WebhookRequest]:
        """Get all stored requests, newest first."""
        reqs = [WebhookRequest.from_dict(d) for d in self._load()]
        return sorted(reqs, key=lambda r: r.timestamp, reverse=True)

    def get_by_id(self, req_id: str) -> WebhookRequest | None:
        """Get a specific request by ID."""
        for d in self._load():
            if d.get("id") == req_id:
                return WebhookRequest.from_dict(d)
        return None

    def filter_by_method(self, method: str) -> list[WebhookRequest]:
        """Filter requests by HTTP method."""
        return [r for r in self.get_all() if r.method.upper() == method.upper()]

    def filter_by_path(self, path: str) -> list[WebhookRequest]:
        """Filter requests by path."""
        return [r for r in self.get_all() if path in r.path]

    def clear(self):
        """Clear all stored requests."""
        self._save([])

    def count(self) -> int:
        """Count stored requests."""
        return len(self._load())

    def export_json(self) -> str:
        """Export all requests as formatted JSON."""
        return json.dumps(self._load(), indent=2)

    def export_markdown(self) -> str:
        """Export all requests as Markdown."""
        requests = self.get_all()
        lines = [
            f"# Webhook Capture Log — {len(requests)} requests",
            "",
        ]

        for req in requests:
            lines.append(f"## {req.method} {req.path}")
            lines.append(f"**ID:** `{req.id}` | **Time:** {req.timestamp} | **From:** {req.source_ip}")
            lines.append(f"**Content-Type:** {req.content_type}")
            lines.append("")

            if req.headers:
                lines.append("**Headers:**")
                for k, v in req.headers.items():
                    lines.append(f"- `{k}`: `{v}`")
                lines.append("")

            if req.query_params:
                lines.append("**Query Params:**")
                for k, v in req.query_params.items():
                    lines.append(f"- `{k}` = `{v}`")
                lines.append("")

            if req.body:
                lines.append("**Body:**")
                lines.append(f"```\n{req.body}\n```")
                lines.append("")

            lines.append("---")
            lines.append("")

        return "\n".join(lines)
