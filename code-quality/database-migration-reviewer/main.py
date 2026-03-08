"""
Database Migration Reviewer — validates migration SQL for safety and best practices.
Usage: python main.py <migration.sql>
"""
import argparse
import sys
import re
import os


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[DB Migration Reviewer] Ready.\n\nPaste a SQL migration to review for destructive operations, missing rollbacks, naming conventions, and ordering issues."


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
    findings = []
    for pattern, severity, message in ISSUES:
        if re.search(pattern, sql, re.IGNORECASE):
            icon = {"critical": "🚨", "high": "⛔", "medium": "⚠️", "low": "ℹ️"}[severity]
            findings.append(f"{icon} [{severity.upper()}] {message}")

    has_rollback = bool(re.search(r"\bROLLBACK\b|\bDOWN\b|-- down|-- rollback", sql, re.IGNORECASE))
    if not has_rollback:
        findings.append("⚠️  [MEDIUM] No rollback/DOWN section detected — ensure you have a revert path.")

    if not findings:
        findings.append("✅ Migration looks safe. No critical issues found.")

    return findings


def main():
    parser = argparse.ArgumentParser(description="Review database migrations for safety")
    parser.add_argument("input", nargs="?", help="Migration .sql file path or raw SQL")
    args = parser.parse_args()

    if not args.input:
        print("Database Migration Reviewer")
        print("Usage: python main.py <migration.sql>")
        sys.exit(0)

    sql = ""
    if os.path.isfile(args.input):
        with open(args.input) as f:
            sql = f.read()
    else:
        sql = args.input

    findings = review_migration(sql)
    print("\n🗄️  Migration Review Report:")
    for f in findings:
        print(f"  {f}")


if __name__ == "__main__":
    main()
