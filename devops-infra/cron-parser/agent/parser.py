"""Cron parser — parse, validate, and describe cron expressions."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

FIELDS = ["minute", "hour", "day_of_month", "month", "day_of_week"]
PRESETS = {"@yearly": "0 0 1 1 *", "@annually": "0 0 1 1 *", "@monthly": "0 0 1 * *", "@weekly": "0 0 * * 0", "@daily": "0 0 * * *", "@midnight": "0 0 * * *", "@hourly": "0 * * * *"}

@dataclass
class CronResult:
    expression: str = ""; is_valid: bool = True; description: str = ""
    fields: dict = field(default_factory=dict); error: str = ""
    def to_dict(self) -> dict: return {"expression": self.expression, "is_valid": self.is_valid, "description": self.description}

def _describe_field(val: str, name: str) -> str:
    if val == "*": return f"every {name}"
    if "/" in val: parts = val.split("/"); return f"every {parts[1]} {name}s"
    if "-" in val: parts = val.split("-"); return f"{name} {parts[0]} through {parts[1]}"
    if "," in val: return f"{name} {val}"
    return f"{name} {val}"

def parse_cron(expr: str) -> CronResult:
    r = CronResult(expression=expr)
    expr = PRESETS.get(expr.strip(), expr.strip())
    parts = expr.split()
    if len(parts) != 5:
        r.is_valid = False; r.error = f"Expected 5 fields, got {len(parts)}"; return r
    for part in parts:
        if not re.match(r'^[\d\*,\-/]+$', part):
            r.is_valid = False; r.error = f"Invalid field: {part}"; return r
    r.fields = dict(zip(FIELDS, parts))
    descs = [_describe_field(parts[i], FIELDS[i]) for i in range(5)]
    r.description = "At " + ", ".join(d for d in descs if "every" not in d or d != f"every {FIELDS[descs.index(d)]}")
    return r

def is_valid_cron(expr: str) -> bool:
    return parse_cron(expr).is_valid

def next_runs(expr: str, count: int = 5) -> list[str]:
    from datetime import datetime, timedelta
    if not is_valid_cron(expr): return []
    now = datetime.now().replace(second=0, microsecond=0)
    return [(now + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M") for i in range(1, count + 1)]

def explain(expr: str) -> str:
    r = parse_cron(expr)
    if not r.is_valid: return f"Invalid: {r.error}"
    return r.description

def format_result_markdown(r: CronResult) -> str:
    if not r.is_valid: return f"## Cron Parser ❌\n**Error:** {r.error}"
    return f"## Cron Parser ⏰\n**Expression:** `{r.expression}`\n**Meaning:** {r.description}"
