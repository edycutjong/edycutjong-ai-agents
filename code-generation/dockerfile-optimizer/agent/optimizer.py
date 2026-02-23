"""Dockerfile optimizer — analyze and improve Dockerfiles."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

RULES = [
    {"id": "DL3006", "severity": "warning", "pattern": r"^FROM\s+\S+$", "check": lambda line: "FROM" in line and ":" not in line.split()[-1] and line.split()[-1] != "scratch", "message": "Always tag the version of an image explicitly", "fix": "Add a specific tag (e.g., :3.12-slim instead of :latest)"},
    {"id": "DL3008", "severity": "warning", "pattern": None, "check": lambda line: "apt-get install" in line and "--no-install-recommends" not in line, "message": "Pin versions in apt-get install", "fix": "Add --no-install-recommends and pin package versions"},
    {"id": "DL3009", "severity": "info", "pattern": None, "check": lambda line: "apt-get update" in line and "rm -rf /var/lib/apt/lists" not in line, "message": "Delete apt-get lists after installing", "fix": "Add && rm -rf /var/lib/apt/lists/* at the end"},
    {"id": "DL3013", "severity": "warning", "pattern": None, "check": lambda line: "pip install" in line and "==" not in line and "-r" not in line, "message": "Pin versions in pip install", "fix": "Use package==version format"},
    {"id": "DL3018", "severity": "warning", "pattern": None, "check": lambda line: "apk add" in line and "--no-cache" not in line, "message": "Use --no-cache with apk add", "fix": "Add --no-cache flag"},
    {"id": "DL3020", "severity": "error", "pattern": None, "check": lambda line: line.strip().startswith("ADD") and "http" not in line and ".tar" not in line, "message": "Use COPY instead of ADD for files", "fix": "Replace ADD with COPY for non-URL, non-tar files"},
    {"id": "DL3025", "severity": "warning", "pattern": None, "check": lambda line: line.strip().startswith("CMD") and "[" not in line, "message": "Use JSON notation for CMD", "fix": "Use CMD [\"executable\", \"arg1\"] format"},
    {"id": "DL4000", "severity": "error", "pattern": None, "check": lambda line: line.strip().startswith("MAINTAINER"), "message": "MAINTAINER is deprecated, use LABEL", "fix": "Replace with LABEL maintainer=\"name\""},
    {"id": "DL4006", "severity": "warning", "pattern": None, "check": lambda line: "&&" in line and "set -o pipefail" not in line and "pipe" in line.lower(), "message": "Set SHELL with pipefail before piping", "fix": "Add SHELL [\"/bin/bash\", \"-o\", \"pipefail\", \"-c\"]"},
]

LAYER_RULES = [
    {"id": "DL3003", "check": lambda instructions: sum(1 for i in instructions if i.startswith("RUN")) > 10, "message": "Too many RUN instructions — combine with &&", "severity": "warning"},
    {"id": "DL3001", "check": lambda instructions: not any("WORKDIR" in i for i in instructions), "message": "Missing WORKDIR instruction", "severity": "info"},
    {"id": "SC001", "check": lambda instructions: instructions and not instructions[0].startswith("FROM"), "message": "First instruction should be FROM", "severity": "error"},
    {"id": "SC002", "check": lambda instructions: sum(1 for i in instructions if i.startswith("COPY")) > 1 and any("COPY . " in i or "COPY ./" in i for i in instructions), "message": "Consider using .dockerignore and multi-stage COPY", "severity": "info"},
]

@dataclass
class LintIssue:
    rule_id: str
    severity: str
    line: int
    message: str
    fix: str = ""
    def to_dict(self) -> dict:
        return {"rule": self.rule_id, "severity": self.severity, "line": self.line, "message": self.message, "fix": self.fix}

@dataclass
class AnalysisResult:
    issues: list[LintIssue] = field(default_factory=list)
    instructions: list[str] = field(default_factory=list)
    stages: int = 0
    layer_count: int = 0
    has_healthcheck: bool = False
    has_user: bool = False
    estimated_layers: int = 0

    @property
    def score(self) -> int:
        s = 100
        for i in self.issues:
            if i.severity == "error": s -= 15
            elif i.severity == "warning": s -= 8
            else: s -= 3
        if not self.has_healthcheck: s -= 5
        if not self.has_user: s -= 5
        return max(0, min(100, s))

    def to_dict(self) -> dict:
        return {"score": self.score, "issues": [i.to_dict() for i in self.issues], "stages": self.stages,
                "layer_count": self.layer_count, "has_healthcheck": self.has_healthcheck, "has_user": self.has_user}


def analyze_dockerfile(content: str) -> AnalysisResult:
    """Analyze a Dockerfile for best practices."""
    result = AnalysisResult()
    lines = content.strip().split("\n")
    instructions = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        instructions.append(stripped)
        if stripped.startswith("FROM"):
            result.stages += 1
        if stripped.startswith("HEALTHCHECK"):
            result.has_healthcheck = True
        if stripped.startswith("USER"):
            result.has_user = True

        for rule in RULES:
            try:
                if rule["check"](stripped):
                    result.issues.append(LintIssue(rule_id=rule["id"], severity=rule["severity"], line=i, message=rule["message"], fix=rule.get("fix", "")))
            except Exception:
                pass

    result.instructions = instructions
    result.layer_count = sum(1 for i in instructions if i.startswith(("RUN", "COPY", "ADD")))
    result.estimated_layers = result.layer_count + result.stages

    for rule in LAYER_RULES:
        if rule["check"](instructions):
            result.issues.append(LintIssue(rule_id=rule["id"], severity=rule["severity"], line=0, message=rule["message"]))

    return result


def format_analysis_markdown(result: AnalysisResult) -> str:
    bar = "█" * (result.score // 10) + "░" * (10 - result.score // 10)
    lines = [
        "# Dockerfile Analysis",
        f"**Score:** {result.score}/100 [{bar}]",
        f"**Stages:** {result.stages} | **Layers:** ~{result.estimated_layers} | **Instructions:** {len(result.instructions)}",
        f"**Healthcheck:** {'✅' if result.has_healthcheck else '❌'} | **Non-root User:** {'✅' if result.has_user else '❌'}",
        "",
    ]
    if result.issues:
        lines.append("## Issues")
        for i in sorted(result.issues, key=lambda x: {"error": 0, "warning": 1, "info": 2}[x.severity]):
            emoji = {"error": "🔴", "warning": "🟡", "info": "🔵"}[i.severity]
            loc = f"L{i.line}" if i.line else "global"
            lines.append(f"- {emoji} **[{i.rule_id}]** {i.message} ({loc})")
            if i.fix: lines.append(f"  - 💡 {i.fix}")
    return "\n".join(lines)
