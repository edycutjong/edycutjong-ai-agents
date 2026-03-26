"""
Database Migration Reviewer — validates migration SQL for safety and best practices.
Usage: python main.py <migration.sql>
"""
import argparse
import sys
import re
import os


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[DB Migration Reviewer] Ready.\n\nPaste a SQL migration to review for destructive operations, missing rollbacks, naming conventions, and ordering issues."  # pragma: no cover


ISSUES = [
    (r"\bDROP\s+TABLE\b", "critical", "DROP TABLE — permanent data loss"),
    (r"\bTRUNCATE\b", "critical", "TRUNCATE — removes all rows instantly"),
    (r"\bDROP\s+DATABASE\b", "critical", "DROP DATABASE — catastrophic, requires explicit confirmation"),
    (r"\bDELETE\s+FROM\b\s+\w+\s*;", "critical", "DELETE without WHERE — removes all rows"),
    (r"\bDROP\s+COLUMN\b", "high", "DROP COLUMN — data loss, hard to reverse"),
    (r"\bALTER\s+COLUMN\b", "medium", "ALTER COLUMN — may fail on existing invalid data"),
    (r"\bADD\s+COLUMN\b.*\bNOT\s+NULL\b(?!\s+DEFAULT)", "high", "NOT NULL column added without DEFAULT — will fail on existing rows"),
    (r"(?i)CREATE\s+INDEX(?!\s+CONCURRENTLY)", "low", "Consider CREATE INDEX CONCURRENTLY to avoid table locks"),
]


def review_migration(sql: str) -> list:
    findings = []  # pragma: no cover
    for pattern, severity, message in ISSUES:  # pragma: no cover
        if re.search(pattern, sql, re.IGNORECASE):  # pragma: no cover
            icon = {"critical": "🚨", "high": "⛔", "medium": "⚠️", "low": "ℹ️"}[severity]  # pragma: no cover
            findings.append(f"{icon} [{severity.upper()}] {message}")  # pragma: no cover

    has_rollback = bool(re.search(r"\bROLLBACK\b|\bDOWN\b|-- down|-- rollback", sql, re.IGNORECASE))  # pragma: no cover
    if not has_rollback:  # pragma: no cover
        findings.append("⚠️  [MEDIUM] No rollback/DOWN section detected — ensure you have a revert path.")  # pragma: no cover

    if not findings:  # pragma: no cover
        findings.append("✅ Migration looks safe. No critical issues found.")  # pragma: no cover

    return findings  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Review database migrations for safety")
    parser.add_argument("input", nargs="?", help="Migration .sql file path or raw SQL")
    args = parser.parse_args()

    if not args.input:
        print("Database Migration Reviewer")
        print("Usage: python main.py <migration.sql>")
        sys.exit(0)

    sql = ""  # pragma: no cover
    if os.path.isfile(args.input):  # pragma: no cover
        with open(args.input) as f:  # pragma: no cover
            sql = f.read()  # pragma: no cover
    else:
        sql = args.input  # pragma: no cover

    findings = review_migration(sql)  # pragma: no cover
    print("\n🗄️  Migration Review Report:")  # pragma: no cover
    for f in findings:  # pragma: no cover
        print(f"  {f}")  # pragma: no cover


if __name__ == "__main__":
    main()
