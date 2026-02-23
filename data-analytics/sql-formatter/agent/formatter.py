"""SQL formatter — format, validate, and analyze SQL queries."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

KEYWORDS = {"SELECT", "FROM", "WHERE", "JOIN", "LEFT", "RIGHT", "INNER", "OUTER", "ON", "AND", "OR", "ORDER", "BY", "GROUP", "HAVING", "LIMIT", "OFFSET", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE", "CREATE", "TABLE", "ALTER", "DROP", "INDEX", "AS", "IN", "NOT", "NULL", "IS", "LIKE", "BETWEEN", "EXISTS", "UNION", "ALL", "DISTINCT", "CASE", "WHEN", "THEN", "ELSE", "END", "COUNT", "SUM", "AVG", "MIN", "MAX"}

@dataclass
class SQLResult:
    original: str = ""; formatted: str = ""; is_valid: bool = True
    tables: list[str] = field(default_factory=list); query_type: str = ""
    keyword_count: int = 0; error: str = ""
    def to_dict(self) -> dict: return {"query_type": self.query_type, "tables": self.tables, "is_valid": self.is_valid}

def format_sql(sql: str) -> SQLResult:
    r = SQLResult(original=sql)
    sql_clean = sql.strip().rstrip(";")
    if not sql_clean: r.is_valid = False; r.error = "Empty query"; return r
    # Detect query type
    first_word = sql_clean.split()[0].upper() if sql_clean.split() else ""
    r.query_type = first_word if first_word in {"SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP"} else "UNKNOWN"
    # Extract tables
    r.tables = list(set(re.findall(r'(?:FROM|JOIN|INTO|UPDATE|TABLE)\s+(\w+)', sql_clean, re.IGNORECASE)))
    # Count keywords
    words = re.findall(r'\b\w+\b', sql_clean.upper())
    r.keyword_count = sum(1 for w in words if w in KEYWORDS)
    # Format
    formatted = sql_clean
    for kw in ["SELECT", "FROM", "WHERE", "JOIN", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "ORDER BY", "GROUP BY", "HAVING", "LIMIT", "UNION"]:
        formatted = re.sub(rf'\b{kw}\b', f'\n{kw}', formatted, flags=re.IGNORECASE)
    formatted = re.sub(r',\s*', ',\n  ', formatted)
    r.formatted = formatted.strip()
    return r

def extract_columns(sql: str) -> list[str]:
    m = re.search(r'SELECT\s+(.*?)\s+FROM', sql, re.IGNORECASE | re.DOTALL)
    if not m: return []
    cols = [c.strip() for c in m.group(1).split(",")]
    return [c.split()[-1] if " " in c else c for c in cols]

def detect_sql_injection(sql: str) -> list[str]:
    risks = []
    if re.search(r"'\s*OR\s+'", sql, re.IGNORECASE): risks.append("OR injection pattern")
    if re.search(r'--\s', sql): risks.append("Comment injection")
    if re.search(r';\s*DROP\s', sql, re.IGNORECASE): risks.append("DROP injection")
    if re.search(r'UNION\s+SELECT', sql, re.IGNORECASE): risks.append("UNION SELECT injection")
    return risks

def format_result_markdown(r: SQLResult) -> str:
    if not r.is_valid: return f"## SQL Formatter ❌\n**Error:** {r.error}"
    return f"## SQL Formatter ✅\n**Type:** {r.query_type} | **Tables:** {', '.join(r.tables)} | **Keywords:** {r.keyword_count}\n```sql\n{r.formatted}\n```"
