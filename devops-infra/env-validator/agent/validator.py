"""Env file validator — validate and parse .env files for correctness."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

@dataclass
class EnvVar:
    key: str = ""; value: str = ""; line: int = 0; quoted: bool = False; is_empty: bool = False

@dataclass
class EnvResult:
    variables: list[EnvVar] = field(default_factory=list); issues: list[str] = field(default_factory=list)
    count: int = 0; empty_count: int = 0; is_valid: bool = True
    def to_dict(self) -> dict: return {"count": self.count, "empty_count": self.empty_count, "is_valid": self.is_valid}

SENSITIVE_PATTERNS = re.compile(r'(?i)(secret|password|key|token|api|auth|pass|credential)', re.IGNORECASE)
KEY_RE = re.compile(r'^[A-Z_][A-Z0-9_]*$')

def parse_env(text: str) -> EnvResult:
    r = EnvResult()
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"): continue
        if "=" not in stripped:
            r.issues.append(f"Line {i}: No '=' found: {stripped[:50]}"); r.is_valid = False; continue
        key, _, value = stripped.partition("=")
        key = key.strip(); value = value.strip()
        quoted = (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'"))
        if quoted: value = value[1:-1]
        var = EnvVar(key=key, value=value, line=i, quoted=quoted, is_empty=not value)
        if not KEY_RE.match(key):
            r.issues.append(f"Line {i}: Invalid key format '{key}' (use UPPER_SNAKE_CASE)")
        if not value: r.empty_count += 1
        r.variables.append(var)
    r.count = len(r.variables)
    return r

def check_required(env: EnvResult, required: list[str]) -> list[str]:
    keys = {v.key for v in env.variables}
    return [k for k in required if k not in keys]

def redact_sensitive(env: EnvResult) -> dict:
    result = {}
    for v in env.variables:
        if SENSITIVE_PATTERNS.search(v.key): result[v.key] = "***REDACTED***"
        else: result[v.key] = v.value
    return result

def to_dict(env: EnvResult) -> dict:
    return {v.key: v.value for v in env.variables}

def compare_envs(env1: EnvResult, env2: EnvResult) -> dict:
    keys1 = {v.key for v in env1.variables}; keys2 = {v.key for v in env2.variables}
    return {"only_in_first": list(keys1 - keys2), "only_in_second": list(keys2 - keys1), "in_both": list(keys1 & keys2)}

def format_result_markdown(r: EnvResult) -> str:
    emoji = "✅" if r.is_valid else "❌"
    lines = [f"## Env Validator {emoji}", f"**Variables:** {r.count} | **Empty:** {r.empty_count}", ""]
    if r.issues:
        lines.append("### Issues")
        for issue in r.issues: lines.append(f"- ❌ {issue}")
    return "\n".join(lines)
