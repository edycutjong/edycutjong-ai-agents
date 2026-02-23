"""License compliance checker — analyze project dependencies for license compatibility."""
from __future__ import annotations
import json, re, os
from dataclasses import dataclass, field

@dataclass
class LicenseInfo:
    name: str
    license: str
    category: str = "unknown"  # permissive, copyleft, restrictive, unknown
    compatible: bool = True
    def to_dict(self) -> dict: return self.__dict__.copy()

LICENSE_DB = {
    "MIT": {"category": "permissive", "osi": True, "copyleft": False},
    "Apache-2.0": {"category": "permissive", "osi": True, "copyleft": False},
    "BSD-2-Clause": {"category": "permissive", "osi": True, "copyleft": False},
    "BSD-3-Clause": {"category": "permissive", "osi": True, "copyleft": False},
    "ISC": {"category": "permissive", "osi": True, "copyleft": False},
    "0BSD": {"category": "permissive", "osi": True, "copyleft": False},
    "Unlicense": {"category": "permissive", "osi": True, "copyleft": False},
    "CC0-1.0": {"category": "permissive", "osi": False, "copyleft": False},
    "GPL-2.0": {"category": "copyleft", "osi": True, "copyleft": True},
    "GPL-3.0": {"category": "copyleft", "osi": True, "copyleft": True},
    "LGPL-2.1": {"category": "copyleft", "osi": True, "copyleft": True},
    "LGPL-3.0": {"category": "copyleft", "osi": True, "copyleft": True},
    "MPL-2.0": {"category": "copyleft", "osi": True, "copyleft": True},
    "AGPL-3.0": {"category": "restrictive", "osi": True, "copyleft": True},
    "SSPL": {"category": "restrictive", "osi": False, "copyleft": True},
    "BSL-1.1": {"category": "restrictive", "osi": False, "copyleft": False},
    "EUPL-1.2": {"category": "copyleft", "osi": True, "copyleft": True},
}

COMPATIBILITY_MATRIX = {
    "MIT": {"permissive": True, "copyleft": True, "restrictive": True},
    "Apache-2.0": {"permissive": True, "copyleft": True, "restrictive": True},
    "GPL-3.0": {"permissive": True, "copyleft": True, "restrictive": False},
    "AGPL-3.0": {"permissive": True, "copyleft": True, "restrictive": False},
}

def normalize_license(text: str) -> str:
    """Normalize common license name variations."""
    text = text.strip()
    mappings = {"MIT License": "MIT", "Apache License 2.0": "Apache-2.0", "BSD 2-Clause": "BSD-2-Clause", "BSD 3-Clause": "BSD-3-Clause", "GNU GPLv3": "GPL-3.0", "GNU GPLv2": "GPL-2.0", "ISC License": "ISC", "The Unlicense": "Unlicense"}
    return mappings.get(text, text)

def classify_license(license_name: str) -> str:
    normalized = normalize_license(license_name)
    info = LICENSE_DB.get(normalized, {})
    return info.get("category", "unknown")

def check_compatibility(project_license: str, dep_licenses: list[LicenseInfo]) -> list[dict]:
    """Check if dependencies are compatible with the project license."""
    issues = []
    proj_cat = classify_license(project_license)
    for dep in dep_licenses:
        dep_cat = classify_license(dep.license)
        dep.category = dep_cat
        if proj_cat == "permissive" and dep_cat in ("copyleft", "restrictive"):
            issues.append({"dependency": dep.name, "license": dep.license, "issue": f"{dep.license} ({dep_cat}) may not be compatible with {project_license} ({proj_cat})"})
            dep.compatible = False
    return issues

def parse_package_json(text: str) -> list[LicenseInfo]:
    """Parse package.json dependencies (simplified)."""
    try:
        pkg = json.loads(text)
        deps = list(pkg.get("dependencies", {}).keys()) + list(pkg.get("devDependencies", {}).keys())
        return [LicenseInfo(name=d, license="unknown") for d in deps]
    except: return []

def parse_requirements_txt(text: str) -> list[LicenseInfo]:
    deps = []
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"): continue
        name = re.split(r"[>=<!\[]", line)[0].strip()
        if name: deps.append(LicenseInfo(name=name, license="unknown"))
    return deps

def format_report_markdown(project_license: str, deps: list[LicenseInfo], issues: list[dict]) -> str:
    emoji = "✅" if not issues else "⚠️"
    lines = [f"# License Compliance Report {emoji}", f"**Project License:** {project_license} | **Dependencies:** {len(deps)} | **Issues:** {len(issues)}", ""]
    if issues:
        lines.append("## ⚠️ Compatibility Issues")
        for i in issues: lines.append(f"- **{i['dependency']}** ({i['license']}): {i['issue']}")
        lines.append("")
    cats = {}
    for d in deps:
        cats.setdefault(d.category, []).append(d)
    for cat in ["permissive", "copyleft", "restrictive", "unknown"]:
        if cat in cats:
            lines.append(f"### {cat.title()} ({len(cats[cat])})")
            for d in cats[cat]: lines.append(f"- {d.name}: `{d.license}`")
            lines.append("")
    return "\n".join(lines)
