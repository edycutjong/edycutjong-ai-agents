"""Dependency updater — analyze and suggest updates for project dependencies."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

@dataclass
class Dependency:
    name: str
    current_version: str = ""
    constraint: str = ""  # ==, >=, ~=, ^
    source_file: str = ""
    is_dev: bool = False

@dataclass
class UpdateResult:
    total_deps: int = 0
    pinned: int = 0
    unpinned: int = 0
    dev_deps: int = 0
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    dependencies: list[Dependency] = field(default_factory=list)
    def to_dict(self) -> dict:
        return {"total_deps": self.total_deps, "pinned": self.pinned, "unpinned": self.unpinned, "issues": len(self.issues)}

def parse_requirements(text: str, filename: str = "requirements.txt") -> list[Dependency]:
    deps = []
    is_dev = "dev" in filename.lower()
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"): continue
        m = re.match(r'^([a-zA-Z0-9_.-]+)\s*(==|>=|<=|~=|\^|!=|>|<)?\s*(.*)$', line)
        if m:
            name, constraint, version = m.group(1), m.group(2) or "", m.group(3).strip()
            deps.append(Dependency(name=name, current_version=version, constraint=constraint, source_file=filename, is_dev=is_dev))
    return deps

def parse_package_json(data: dict) -> list[Dependency]:
    deps = []
    for name, version in data.get("dependencies", {}).items():
        constraint = ""
        ver = version
        if version.startswith("^"): constraint = "^"; ver = version[1:]
        elif version.startswith("~"): constraint = "~"; ver = version[1:]
        deps.append(Dependency(name=name, current_version=ver, constraint=constraint, source_file="package.json"))
    for name, version in data.get("devDependencies", {}).items():
        constraint = ""
        ver = version
        if version.startswith("^"): constraint = "^"; ver = version[1:]
        elif version.startswith("~"): constraint = "~"; ver = version[1:]
        deps.append(Dependency(name=name, current_version=ver, constraint=constraint, source_file="package.json", is_dev=True))
    return deps

def analyze_dependencies(deps: list[Dependency]) -> UpdateResult:
    r = UpdateResult(total_deps=len(deps), dependencies=deps)
    for d in deps:
        if d.is_dev: r.dev_deps += 1
        if d.constraint == "==" or (d.current_version and not d.constraint):
            r.pinned += 1
        else:
            r.unpinned += 1
    # Issues
    if r.unpinned > 0 and r.pinned == 0:
        r.issues.append("No dependencies are pinned — builds may be non-reproducible")
    if r.total_deps > 50:
        r.issues.append(f"Large dependency count ({r.total_deps}) — consider auditing")
    # Check for common security concerns
    risky = {"requests": "Ensure using HTTPS only", "pyyaml": "Use safe_load, not load", "pickle": "Unsafe deserialization"}
    for d in deps:
        if d.name.lower() in risky:
            r.suggestions.append(f"{d.name}: {risky[d.name.lower()]}")
    no_version = [d for d in deps if not d.current_version and not d.constraint]
    if no_version:
        r.issues.append(f"{len(no_version)} deps without version constraints")
        r.suggestions.append("Pin all dependencies for reproducible builds")
    return r

def format_result_markdown(r: UpdateResult) -> str:
    lines = ["## Dependency Analysis", f"**Total:** {r.total_deps} | **Pinned:** {r.pinned} | **Unpinned:** {r.unpinned} | **Dev:** {r.dev_deps}", ""]
    if r.issues:
        lines.append("### Issues")
        for i in r.issues: lines.append(f"- ⚠️ {i}")
        lines.append("")
    if r.suggestions:
        lines.append("### Suggestions")
        for s in r.suggestions: lines.append(f"- 💡 {s}")
    if not r.issues and not r.suggestions:
        lines.append("✅ Dependencies look good!")
    return "\n".join(lines)
