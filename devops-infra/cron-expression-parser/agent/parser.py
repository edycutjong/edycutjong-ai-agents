"""Cron expression parser — parse and explain cron schedules."""
from __future__ import annotations
from dataclasses import dataclass, field

FIELD_NAMES = ["minute", "hour", "day_of_month", "month", "day_of_week"]
FIELD_RANGES = {"minute": (0, 59), "hour": (0, 23), "day_of_month": (1, 31), "month": (1, 12), "day_of_week": (0, 6)}
MONTH_NAMES = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
DAY_NAMES = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
PRESETS = {"@yearly": "0 0 1 1 *", "@annually": "0 0 1 1 *", "@monthly": "0 0 1 * *", "@weekly": "0 0 * * 0", "@daily": "0 0 * * *", "@midnight": "0 0 * * *", "@hourly": "0 * * * *"}

@dataclass
class CronField:
    raw: str = ""
    name: str = ""
    values: list[int] = field(default_factory=list)
    is_wildcard: bool = False
    description: str = ""

@dataclass
class CronResult:
    expression: str = ""
    is_valid: bool = True
    error: str = ""
    fields: list[CronField] = field(default_factory=list)
    description: str = ""
    def to_dict(self) -> dict:
        return {"expression": self.expression, "is_valid": self.is_valid, "description": self.description}

def parse_field(raw: str, name: str) -> CronField:
    f = CronField(raw=raw, name=name)
    lo, hi = FIELD_RANGES[name]
    if raw == "*":
        f.is_wildcard = True
        f.description = f"every {name.replace('_', ' ')}"
        return f
    values = set()
    for part in raw.split(","):
        if "/" in part:
            base, step = part.split("/", 1)
            step = int(step)
            start = lo if base == "*" else int(base)
            values.update(range(start, hi + 1, step))
            f.description = f"every {step} {name.replace('_', ' ')}s"
        elif "-" in part:
            a, b = part.split("-", 1)
            values.update(range(int(a), int(b) + 1))
            f.description = f"{name.replace('_', ' ')} {a} through {b}"
        else:
            values.add(int(part))
    f.values = sorted(values)
    if not f.description:
        if name == "month": f.description = f"in {', '.join(MONTH_NAMES.get(v, str(v)) for v in f.values)}"
        elif name == "day_of_week": f.description = f"on {', '.join(DAY_NAMES.get(v, str(v)) for v in f.values)}"
        else: f.description = f"at {name.replace('_', ' ')} {', '.join(str(v) for v in f.values)}"
    return f

def parse_cron(expression: str) -> CronResult:
    r = CronResult(expression=expression)
    expr = PRESETS.get(expression.strip().lower(), expression.strip())
    parts = expr.split()
    if len(parts) != 5:
        r.is_valid = False
        r.error = f"Expected 5 fields, got {len(parts)}"
        return r
    try:
        for i, part in enumerate(parts):
            r.fields.append(parse_field(part, FIELD_NAMES[i]))
    except (ValueError, IndexError) as e:
        r.is_valid = False
        r.error = str(e)
        return r
    descs = [f.description for f in r.fields if not f.is_wildcard]
    r.description = "Runs " + (", ".join(descs) if descs else "every minute")
    return r

def validate_cron(expression: str) -> tuple[bool, str]:
    r = parse_cron(expression)
    return r.is_valid, r.error

def get_next_descriptions(expression: str) -> str:
    r = parse_cron(expression)
    if not r.is_valid: return f"Invalid: {r.error}"
    return r.description

def format_result_markdown(r: CronResult) -> str:
    if not r.is_valid:
        return f"## Cron Expression ❌\n**Expression:** `{r.expression}`\n**Error:** {r.error}"
    lines = [f"## Cron Expression ✅", f"**Expression:** `{r.expression}`", f"**Schedule:** {r.description}", "", "### Fields"]
    for f in r.fields:
        val = "*" if f.is_wildcard else ", ".join(str(v) for v in f.values)
        lines.append(f"| `{f.raw}` | {f.name.replace('_', ' ')} | {f.description} |")
    return "\n".join(lines)
