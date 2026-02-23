"""Dependency checker — analyze requirements.txt and detect outdated/conflicting packages."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

@dataclass
class Package:
    name: str = ""; version: str = ""; operator: str = "=="; is_pinned: bool = False

@dataclass
class DepResult:
    packages: list[Package] = field(default_factory=list); total: int = 0; pinned: int = 0
    unpinned: int = 0; duplicates: list[str] = field(default_factory=list); is_valid: bool = True; error: str = ""
    def to_dict(self) -> dict: return {"total": self.total, "pinned": self.pinned, "unpinned": self.unpinned}

def parse_requirements(text: str) -> DepResult:
    r = DepResult()
    seen = {}
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"): continue
        m = re.match(r'^([a-zA-Z0-9_.-]+)\s*(==|>=|<=|!=|~=|>|<)?\s*(.*)$', line)
        if m:
            name, op, ver = m.group(1).lower(), m.group(2) or "", m.group(3) or ""
            pkg = Package(name=name, version=ver, operator=op, is_pinned=op == "==")
            r.packages.append(pkg)
            if name in seen: r.duplicates.append(name)
            seen[name] = True
    r.total = len(r.packages)
    r.pinned = sum(1 for p in r.packages if p.is_pinned)
    r.unpinned = r.total - r.pinned
    return r

def find_conflicts(text: str) -> list[str]:
    r = parse_requirements(text)
    return r.duplicates

def get_package_names(text: str) -> list[str]:
    r = parse_requirements(text)
    return [p.name for p in r.packages]

def check_security(packages: list[str]) -> list[str]:
    KNOWN_VULN = {"django<2.0", "flask<1.0", "requests<2.20", "urllib3<1.24"}
    return [p for p in packages if any(p.lower().startswith(v.split("<")[0]) for v in KNOWN_VULN)]

def generate_requirements(packages: dict[str, str]) -> str:
    return "\n".join(f"{name}=={ver}" for name, ver in sorted(packages.items()))

def format_result_markdown(r: DepResult) -> str:
    if not r.is_valid: return f"## Dependency Checker ❌\n**Error:** {r.error}"
    return f"## Dependency Checker 📦\n**Total:** {r.total} | **Pinned:** {r.pinned} | **Unpinned:** {r.unpinned}"
