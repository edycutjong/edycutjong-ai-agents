"""SQL query optimizer — analyze and suggest improvements for SQL queries."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

@dataclass
class QueryAnalysis:
    query: str = ""
    query_type: str = ""  # SELECT, INSERT, UPDATE, DELETE
    tables: list[str] = field(default_factory=list)
    has_where: bool = False
    has_index_hint: bool = False
    has_select_star: bool = False
    has_subquery: bool = False
    has_join: bool = False
    join_count: int = 0
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    score: int = 100  # starts perfect, deduct for issues

def detect_query_type(query: str) -> str:
    q = query.strip().upper()
    for t in ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP"]:
        if q.startswith(t): return t
    return "UNKNOWN"

def extract_tables(query: str) -> list[str]:
    tables = []
    patterns = [r"\bFROM\s+(\w+)", r"\bJOIN\s+(\w+)", r"\bINTO\s+(\w+)", r"\bUPDATE\s+(\w+)"]
    for p in patterns:
        tables.extend(re.findall(p, query, re.I))
    return list(set(tables))

def analyze_query(query: str) -> QueryAnalysis:
    a = QueryAnalysis(query=query)
    q_upper = query.upper()
    a.query_type = detect_query_type(query)
    a.tables = extract_tables(query)
    a.has_where = bool(re.search(r"\bWHERE\b", q_upper))
    a.has_select_star = bool(re.search(r"SELECT\s+\*", q_upper))
    a.has_subquery = q_upper.count("SELECT") > 1
    a.has_join = bool(re.search(r"\bJOIN\b", q_upper))
    a.join_count = len(re.findall(r"\bJOIN\b", q_upper))
    # Issues & suggestions
    if a.has_select_star:
        a.issues.append("Using SELECT * — fetches all columns")
        a.suggestions.append("Specify only needed columns")
        a.score -= 15
    if a.query_type in ("SELECT", "UPDATE", "DELETE") and not a.has_where:
        a.issues.append("No WHERE clause — affects all rows")
        a.suggestions.append("Add a WHERE clause to limit scope")
        a.score -= 25
    if a.has_subquery:
        a.issues.append("Contains subquery — may be slow")
        a.suggestions.append("Consider using JOINs or CTEs instead")
        a.score -= 10
    if a.join_count > 3:
        a.issues.append(f"{a.join_count} JOINs detected — complex query")
        a.suggestions.append("Consider breaking into smaller queries or using views")
        a.score -= 10
    if re.search(r"\bLIKE\s+'%", q_upper):
        a.issues.append("LIKE with leading wildcard — prevents index use")
        a.suggestions.append("Avoid leading % in LIKE patterns")
        a.score -= 15
    if re.search(r"\bORDER BY\b", q_upper) and not re.search(r"\bLIMIT\b", q_upper):
        a.issues.append("ORDER BY without LIMIT — sorts all rows")
        a.suggestions.append("Add LIMIT to reduce sorted result set")
        a.score -= 10
    if re.search(r"\bDISTINCT\b", q_upper):
        a.issues.append("DISTINCT may indicate data model issues")
        a.suggestions.append("Review if DISTINCT is necessary or fix JOINs")
        a.score -= 5
    if not re.search(r"\bINDEX\b", q_upper) and len(a.tables) > 0 and a.has_where:
        a.suggestions.append("Ensure WHERE columns are indexed")
    a.score = max(0, a.score)
    return a

def format_analysis_markdown(a: QueryAnalysis) -> str:
    emoji = "🟢" if a.score >= 80 else "🟡" if a.score >= 50 else "🔴"
    lines = [f"## SQL Analysis {emoji}", f"**Type:** {a.query_type} | **Tables:** {', '.join(a.tables) or 'none'} | **Score:** {a.score}/100", ""]
    flags = [("WHERE clause", a.has_where), ("SELECT *", a.has_select_star), ("Subquery", a.has_subquery), ("JOINs", a.has_join)]
    for name, val in flags: lines.append(f"{'✅' if not val or name == 'WHERE clause' else '⚠️'} {name}: {'Yes' if val else 'No'}")
    if a.issues:
        lines.append("\n### Issues")
        for i in a.issues: lines.append(f"- ❌ {i}")
    if a.suggestions:
        lines.append("\n### Suggestions")
        for s in a.suggestions: lines.append(f"- 💡 {s}")
    return "\n".join(lines)
