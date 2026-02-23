"""CSV deduplicator — remove duplicate rows from CSV data."""
from __future__ import annotations
import csv, io, hashlib
from dataclasses import dataclass, field

@dataclass
class DedupeResult:
    total_rows: int = 0
    unique_rows: int = 0
    duplicates_removed: int = 0
    duplicate_groups: int = 0
    columns: list[str] = field(default_factory=list)
    def to_dict(self) -> dict:
        return {"total_rows": self.total_rows, "unique_rows": self.unique_rows, "duplicates_removed": self.duplicates_removed}

def parse_csv(text: str, delimiter: str = ",") -> tuple[list[str], list[list[str]]]:
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    rows = list(reader)
    if not rows: return [], []
    return rows[0], rows[1:]

def row_hash(row: list[str], columns: list[int] | None = None) -> str:
    if columns: key = "|".join(row[i] for i in columns if i < len(row))
    else: key = "|".join(row)
    return hashlib.md5(key.encode()).hexdigest()

def deduplicate(headers: list[str], rows: list[list[str]], key_columns: list[int] | None = None, keep: str = "first") -> tuple[list[list[str]], DedupeResult]:
    result = DedupeResult(total_rows=len(rows), columns=headers)
    seen = {}
    unique = []
    for i, row in enumerate(rows):
        h = row_hash(row, key_columns)
        if h not in seen:
            seen[h] = [i]
            unique.append(row)
        else:
            seen[h].append(i)
    result.unique_rows = len(unique)
    result.duplicates_removed = result.total_rows - result.unique_rows
    result.duplicate_groups = sum(1 for indices in seen.values() if len(indices) > 1)
    return unique, result

def find_duplicates(headers: list[str], rows: list[list[str]], key_columns: list[int] | None = None) -> list[list[list[str]]]:
    groups = {}
    for row in rows:
        h = row_hash(row, key_columns)
        groups.setdefault(h, []).append(row)
    return [group for group in groups.values() if len(group) > 1]

def to_csv_string(headers: list[str], rows: list[list[str]], delimiter: str = ",") -> str:
    out = io.StringIO()
    writer = csv.writer(out, delimiter=delimiter)
    writer.writerow(headers)
    writer.writerows(rows)
    return out.getvalue().strip()

def format_result_markdown(result: DedupeResult) -> str:
    emoji = "✅" if result.duplicates_removed == 0 else "🔄"
    lines = [f"## CSV Deduplication {emoji}", f"**Total:** {result.total_rows} | **Unique:** {result.unique_rows} | **Removed:** {result.duplicates_removed} | **Duplicate groups:** {result.duplicate_groups}"]
    if result.duplicates_removed == 0:
        lines.append("\n✅ No duplicates found!")
    else:
        pct = round(result.duplicates_removed / max(result.total_rows, 1) * 100, 1)
        lines.append(f"\n🔄 Removed {result.duplicates_removed} duplicates ({pct}% of total)")
    return "\n".join(lines)
