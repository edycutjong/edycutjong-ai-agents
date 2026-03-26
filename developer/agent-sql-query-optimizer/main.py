"""
SQL Query Optimizer Agent — analyzes SQL queries and suggests optimizations.
Usage: python main.py <query.sql>
"""
import argparse
import os
import re
import sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[SQL Query Optimizer] Provide a SQL query to get optimization suggestions."


ANTI_PATTERNS = [
    (r"SELECT\s+\*", "SELECT_STAR", "Avoid SELECT * — specify needed columns to reduce I/O", "MEDIUM"),
    (r"(?i)SELECT.*\bIN\s*\(\s*SELECT", "SUBQUERY_IN", "Replace IN (SELECT...) with JOIN for better performance", "HIGH"),
    (r"(?i)WHERE.*\bLIKE\s+'%", "LEADING_WILDCARD", "Leading wildcard '%...' prevents index usage", "HIGH"),
    (r"(?i)ORDER\s+BY\s+\w+\s*,\s*\w+(?!.*LIMIT)", "ORDER_NO_LIMIT", "ORDER BY without LIMIT scans all rows", "MEDIUM"),
    (r"(?i)\bOR\b.*\bOR\b", "MULTIPLE_OR", "Multiple OR conditions — consider UNION or IN clause", "LOW"),
    (r"(?i)SELECT\s+DISTINCT", "DISTINCT_USAGE", "DISTINCT may indicate a missing JOIN condition", "LOW"),
    (r"(?i)\bNOT\s+IN\b", "NOT_IN", "NOT IN can be slow — consider NOT EXISTS or LEFT JOIN IS NULL", "MEDIUM"),
    (r"(?i)WHERE\s+\w+\s*!=", "NOT_EQUALS", "!= prevents index usage on some databases", "LOW"),
    (r"(?i)\bCOUNT\(\*\)\b.*WHERE", "COUNT_WITH_WHERE", "COUNT(*) with WHERE — ensure index covers the filter", "MEDIUM"),
    (r"(?i)(?:CROSS|,)\s*JOIN", "CROSS_JOIN", "Possible cartesian product — verify JOIN condition", "HIGH"),
]


def analyze_query(sql: str) -> list:
    findings = []
    for pattern, code, message, severity in ANTI_PATTERNS:
        if re.search(pattern, sql):
            findings.append({"code": code, "message": message, "severity": severity})

    # Suggest index candidates
    where_cols = re.findall(r"(?i)WHERE\s+(\w+)\s*[=<>!]", sql)
    join_cols = re.findall(r"(?i)(?:ON|USING)\s*\(?(\w+)", sql)
    order_cols = re.findall(r"(?i)ORDER\s+BY\s+(\w+)", sql)
    index_candidates = list(set(where_cols + join_cols + order_cols))
    return findings, index_candidates


def estimate_complexity(sql: str) -> str:
    joins = len(re.findall(r"(?i)\bJOIN\b", sql))
    subqueries = len(re.findall(r"(?i)\(\s*SELECT", sql))
    if joins >= 4 or subqueries >= 2:
        return "HIGH"
    if joins >= 2 or subqueries >= 1:
        return "MEDIUM"
    return "LOW"


def format_report(sql: str, findings: list, index_candidates: list) -> str:
    complexity = estimate_complexity(sql)
    icons = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
    lines = [f"🔍 SQL Analysis — Complexity: {icons.get(complexity, '⚪')} {complexity}\n"]
    if findings:
        lines.append(f"  {len(findings)} optimization(s) found:\n")
        for f in findings:
            icon = icons.get(f["severity"], "⚪")
            lines.append(f"    {icon} [{f['code']}] {f['message']}")
    else:
        lines.append("  ✅ No common anti-patterns detected.")
    if index_candidates:
        lines.append(f"\n  📌 Index candidates: {', '.join(index_candidates)}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="SQL Query Optimizer Agent")
    parser.add_argument("file", nargs="?", help="SQL file or query string")
    args = parser.parse_args()
    if not args.file:
        print("SQL Query Optimizer Agent\nUsage: python main.py <query.sql>")
        sys.exit(0)
    if os.path.isfile(args.file):
        sql = open(args.file).read()
    else:
        sql = args.file
    findings, index_candidates = analyze_query(sql)
    print(format_report(sql, findings, index_candidates))


if __name__ == "__main__":  # pragma: no cover
    main()
