"""API changelog differ — compare OpenAPI/Swagger specs and detect breaking changes."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum


class ChangeType(str, Enum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"
    DEPRECATED = "deprecated"


class Severity(str, Enum):
    BREAKING = "breaking"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Change:
    """A single API change."""
    change_type: str
    severity: str
    path: str
    description: str
    details: str = ""

    def to_dict(self) -> dict:
        return {"type": self.change_type, "severity": self.severity,
                "path": self.path, "description": self.description, "details": self.details}


@dataclass
class DiffResult:
    """Result of comparing two API specs."""
    changes: list[Change] = field(default_factory=list)
    old_version: str = ""
    new_version: str = ""

    @property
    def breaking_count(self) -> int:
        return sum(1 for c in self.changes if c.severity == Severity.BREAKING)

    @property
    def warning_count(self) -> int:
        return sum(1 for c in self.changes if c.severity == Severity.WARNING)

    @property
    def info_count(self) -> int:
        return sum(1 for c in self.changes if c.severity == Severity.INFO)

    def to_dict(self) -> dict:
        return {
            "old_version": self.old_version, "new_version": self.new_version,
            "total_changes": len(self.changes),
            "breaking": self.breaking_count, "warnings": self.warning_count,
            "info": self.info_count,
            "changes": [c.to_dict() for c in self.changes],
        }


def diff_specs(old_spec: dict, new_spec: dict) -> DiffResult:
    """Compare two OpenAPI/Swagger-style specs."""
    result = DiffResult(
        old_version=old_spec.get("info", {}).get("version", "unknown"),
        new_version=new_spec.get("info", {}).get("version", "unknown"),
    )

    old_paths = old_spec.get("paths", {})
    new_paths = new_spec.get("paths", {})

    # Check removed endpoints (BREAKING)
    for path in old_paths:
        if path not in new_paths:
            result.changes.append(Change(
                ChangeType.REMOVED, Severity.BREAKING, path,
                f"Endpoint removed: {path}",
            ))
        else:
            _diff_endpoint(old_paths[path], new_paths[path], path, result)

    # Check added endpoints (INFO)
    for path in new_paths:
        if path not in old_paths:
            methods = ", ".join(m.upper() for m in new_paths[path] if m != "parameters")
            result.changes.append(Change(
                ChangeType.ADDED, Severity.INFO, path,
                f"New endpoint: {path} [{methods}]",
            ))

    # Check schema changes
    old_schemas = old_spec.get("components", {}).get("schemas", old_spec.get("definitions", {}))
    new_schemas = new_spec.get("components", {}).get("schemas", new_spec.get("definitions", {}))
    _diff_schemas(old_schemas, new_schemas, result)

    return result


def _diff_endpoint(old_ep: dict, new_ep: dict, path: str, result: DiffResult):
    """Compare methods within an endpoint."""
    for method in old_ep:
        if method == "parameters":
            continue
        if method not in new_ep:
            result.changes.append(Change(
                ChangeType.REMOVED, Severity.BREAKING, f"{method.upper()} {path}",
                f"Method removed: {method.upper()} {path}",
            ))
        else:
            _diff_method(old_ep[method], new_ep[method], f"{method.upper()} {path}", result)

    for method in new_ep:
        if method == "parameters":
            continue
        if method not in old_ep:
            result.changes.append(Change(
                ChangeType.ADDED, Severity.INFO, f"{method.upper()} {path}",
                f"Method added: {method.upper()} {path}",
            ))


def _diff_method(old_m: dict, new_m: dict, path: str, result: DiffResult):
    """Compare method details (params, responses, deprecated)."""
    # Check deprecation
    if new_m.get("deprecated") and not old_m.get("deprecated"):
        result.changes.append(Change(
            ChangeType.DEPRECATED, Severity.WARNING, path,
            f"Deprecated: {path}",
        ))

    # Check required params added (BREAKING for clients)
    old_params = {p.get("name"): p for p in old_m.get("parameters", [])}
    new_params = {p.get("name"): p for p in new_m.get("parameters", [])}

    for name, param in new_params.items():
        if name not in old_params and param.get("required"):
            result.changes.append(Change(
                ChangeType.ADDED, Severity.BREAKING, path,
                f"New required parameter: {name}",
                details=f"in={param.get('in', 'unknown')}",
            ))
        elif name not in old_params:
            result.changes.append(Change(
                ChangeType.ADDED, Severity.INFO, path,
                f"New optional parameter: {name}",
            ))

    for name in old_params:
        if name not in new_params:
            result.changes.append(Change(
                ChangeType.REMOVED, Severity.BREAKING, path,
                f"Parameter removed: {name}",
            ))

    # Check response changes
    old_resp = set(old_m.get("responses", {}).keys())
    new_resp = set(new_m.get("responses", {}).keys())

    for code in new_resp - old_resp:
        result.changes.append(Change(
            ChangeType.ADDED, Severity.INFO, path,
            f"New response code: {code}",
        ))

    for code in old_resp - new_resp:
        result.changes.append(Change(
            ChangeType.REMOVED, Severity.WARNING, path,
            f"Response code removed: {code}",
        ))


def _diff_schemas(old_schemas: dict, new_schemas: dict, result: DiffResult):
    """Compare schema definitions."""
    for name in old_schemas:
        if name not in new_schemas:
            result.changes.append(Change(
                ChangeType.REMOVED, Severity.BREAKING, f"schema/{name}",
                f"Schema removed: {name}",
            ))
        else:
            old_props = set(old_schemas[name].get("properties", {}).keys())
            new_props = set(new_schemas[name].get("properties", {}).keys())
            old_required = set(old_schemas[name].get("required", []))
            new_required = set(new_schemas[name].get("required", []))

            for prop in old_props - new_props:
                result.changes.append(Change(
                    ChangeType.REMOVED, Severity.BREAKING, f"schema/{name}.{prop}",
                    f"Property removed from {name}: {prop}",
                ))

            for prop in new_props - old_props:
                sev = Severity.BREAKING if prop in new_required else Severity.INFO
                result.changes.append(Change(
                    ChangeType.ADDED, sev, f"schema/{name}.{prop}",
                    f"Property added to {name}: {prop}",
                ))

            for prop in new_required - old_required:
                if prop in old_props:
                    result.changes.append(Change(
                        ChangeType.MODIFIED, Severity.BREAKING, f"schema/{name}.{prop}",
                        f"Property now required in {name}: {prop}",
                    ))

    for name in new_schemas:
        if name not in old_schemas:
            result.changes.append(Change(
                ChangeType.ADDED, Severity.INFO, f"schema/{name}",
                f"New schema: {name}",
            ))


def format_diff_markdown(result: DiffResult) -> str:
    """Format diff as Markdown changelog."""
    lines = [
        f"# API Changelog: {result.old_version} → {result.new_version}",
        "",
        f"**Total Changes:** {len(result.changes)}",
        f"**🔴 Breaking:** {result.breaking_count} | **🟡 Warnings:** {result.warning_count} | **🟢 Info:** {result.info_count}",
        "",
    ]

    for severity_label, severity_val, emoji in [
        ("Breaking Changes", Severity.BREAKING, "🔴"),
        ("Warnings", Severity.WARNING, "🟡"),
        ("New Features & Info", Severity.INFO, "🟢"),
    ]:
        items = [c for c in result.changes if c.severity == severity_val]
        if items:
            lines.append(f"## {emoji} {severity_label}")
            for c in items:
                tag = f"[{c.change_type}]"
                lines.append(f"- {tag} **{c.path}** — {c.description}")
            lines.append("")

    return "\n".join(lines)
