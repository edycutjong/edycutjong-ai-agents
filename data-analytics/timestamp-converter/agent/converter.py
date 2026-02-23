"""Timestamp converter — convert between Unix timestamps, ISO 8601, and human-readable formats."""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass

@dataclass
class TimestampResult:
    unix: float = 0; iso: str = ""; human: str = ""; utc_offset: str = "+00:00"
    day_of_week: str = ""; is_valid: bool = True; error: str = ""
    def to_dict(self) -> dict: return {"unix": self.unix, "iso": self.iso, "human": self.human, "is_valid": self.is_valid}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def unix_to_datetime(ts: float) -> TimestampResult:
    r = TimestampResult(unix=ts)
    try:
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        r.iso = dt.isoformat(); r.human = dt.strftime("%B %d, %Y %H:%M:%S UTC"); r.day_of_week = DAYS[dt.weekday()]
    except Exception as e: r.is_valid = False; r.error = str(e)
    return r

def iso_to_unix(iso_str: str) -> TimestampResult:
    r = TimestampResult()
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        r.unix = dt.timestamp(); r.iso = iso_str; r.human = dt.strftime("%B %d, %Y %H:%M:%S"); r.day_of_week = DAYS[dt.weekday()]
    except Exception as e: r.is_valid = False; r.error = str(e)
    return r

def now_utc() -> TimestampResult:
    return unix_to_datetime(datetime.now(timezone.utc).timestamp())

def time_difference(ts1: float, ts2: float) -> dict:
    diff = abs(ts2 - ts1)
    return {"seconds": diff, "minutes": diff / 60, "hours": diff / 3600, "days": diff / 86400}

def add_time(ts: float, days: int = 0, hours: int = 0, minutes: int = 0) -> TimestampResult:
    new_ts = ts + days * 86400 + hours * 3600 + minutes * 60
    return unix_to_datetime(new_ts)

def is_future(ts: float) -> bool:
    return ts > datetime.now(timezone.utc).timestamp()

def format_relative(ts: float) -> str:
    diff = datetime.now(timezone.utc).timestamp() - ts
    if abs(diff) < 60: return "just now"
    if abs(diff) < 3600: return f"{int(abs(diff)/60)} minutes {'ago' if diff > 0 else 'from now'}"
    if abs(diff) < 86400: return f"{int(abs(diff)/3600)} hours {'ago' if diff > 0 else 'from now'}"
    return f"{int(abs(diff)/86400)} days {'ago' if diff > 0 else 'from now'}"

def format_result_markdown(r: TimestampResult) -> str:
    if not r.is_valid: return f"## Timestamp ❌\n**Error:** {r.error}"
    return f"## Timestamp ✅\n**Unix:** `{r.unix}` | **ISO:** `{r.iso}`\n**Human:** {r.human} ({r.day_of_week})"
