"""CSV analyzer — analyze CSV data with statistics and column profiling."""
from __future__ import annotations
import csv, io, statistics
from dataclasses import dataclass, field
from collections import Counter

@dataclass
class ColumnProfile:
    name: str = ""; dtype: str = ""; unique: int = 0; nulls: int = 0; total: int = 0
    min_val: str = ""; max_val: str = ""; mean: float = 0; top_values: list = field(default_factory=list)

@dataclass
class CSVResult:
    rows: int = 0; columns: int = 0; column_names: list[str] = field(default_factory=list)
    profiles: list[ColumnProfile] = field(default_factory=list); issues: list[str] = field(default_factory=list)
    def to_dict(self) -> dict: return {"rows": self.rows, "columns": self.columns, "column_names": self.column_names}

def detect_type(values: list[str]) -> str:
    nums = sum(1 for v in values if v and _is_number(v))
    if nums > len(values) * 0.8: return "numeric"
    return "string"

def _is_number(s: str) -> bool:
    try: float(s); return True
    except: return False

def profile_column(name: str, values: list[str]) -> ColumnProfile:
    p = ColumnProfile(name=name, total=len(values))
    p.nulls = sum(1 for v in values if not v.strip())
    non_null = [v for v in values if v.strip()]
    p.unique = len(set(non_null))
    p.dtype = detect_type(non_null)
    if non_null:
        counter = Counter(non_null)
        p.top_values = [v for v, _ in counter.most_common(5)]
        if p.dtype == "numeric":
            nums = [float(v) for v in non_null if _is_number(v)]
            if nums: p.min_val = str(min(nums)); p.max_val = str(max(nums)); p.mean = statistics.mean(nums)
        else: p.min_val = min(non_null); p.max_val = max(non_null)
    return p

def analyze_csv(text: str) -> CSVResult:
    r = CSVResult()
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows: return r
    r.column_names = rows[0]; r.columns = len(rows[0]); r.rows = len(rows) - 1
    data = rows[1:]
    for i, col_name in enumerate(r.column_names):
        values = [row[i] if i < len(row) else "" for row in data]
        r.profiles.append(profile_column(col_name, values))
    for row in data:
        if len(row) != r.columns: r.issues.append(f"Row has {len(row)} columns, expected {r.columns}")
    return r

def get_column_stats(text: str, column: str) -> dict:
    r = analyze_csv(text)
    for p in r.profiles:
        if p.name == column: return {"type": p.dtype, "unique": p.unique, "nulls": p.nulls, "mean": p.mean}
    return {}

def format_result_markdown(r: CSVResult) -> str:
    lines = [f"## CSV Analysis 📊", f"**Rows:** {r.rows} | **Columns:** {r.columns}", ""]
    for p in r.profiles:
        lines.append(f"### `{p.name}` ({p.dtype})")
        lines.append(f"- Unique: {p.unique} | Nulls: {p.nulls}")
        if p.dtype == "numeric": lines.append(f"- Range: {p.min_val} - {p.max_val} | Mean: {p.mean:.2f}")
    return "\n".join(lines)
