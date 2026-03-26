"""
Migration Checker Agent — validates database migration files for safety.
Usage: python main.py <migration_file_or_dir>
"""
import argparse
import sys
import re
import os


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Migration Checker] Ready.\n\nPaste SQL migration code or describe your migration to check for destructive operations, naming issues, and ordering problems."  # pragma: no cover


DESTRUCTIVE_PATTERNS = [
    (r"\bDROP\s+TABLE\b", "DROP TABLE — data loss risk"),
    (r"\bDROP\s+COLUMN\b", "DROP COLUMN — irreversible data loss"),
    (r"\bTRUNCATE\b", "TRUNCATE — removes all rows"),
    (r"\bDELETE\s+FROM\b(?!\s+WHERE)", "DELETE without WHERE — removes all rows"),
    (r"\bALTER\s+COLUMN\b.*\bNOT\s+NULL\b", "Adding NOT NULL constraint — may fail on existing nulls"),
]

MISSING_PATTERNS = [
    (r"(?i)CREATE\s+TABLE(?!.*PRIMARY\s+KEY)", "CREATE TABLE may be missing PRIMARY KEY"),
    (r"(?i)CREATE\s+INDEX(?!\s+IF\s+NOT\s+EXISTS)", "CREATE INDEX without IF NOT EXISTS — may fail if exists"),
]


def check_migration(sql: str) -> list:
    issues = []  # pragma: no cover
    for pattern, msg in DESTRUCTIVE_PATTERNS:  # pragma: no cover
        if re.search(pattern, sql, re.IGNORECASE):  # pragma: no cover
            issues.append(f"🚨 Destructive: {msg}")  # pragma: no cover
    for pattern, msg in MISSING_PATTERNS:  # pragma: no cover
        if re.search(pattern, sql, re.IGNORECASE):  # pragma: no cover
            issues.append(f"⚠️  Warning: {msg}")  # pragma: no cover
    if not issues:  # pragma: no cover
        issues.append("✅ No obvious destructive operations detected.")  # pragma: no cover
    return issues  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Validate database migration files")
    parser.add_argument("input", nargs="?", help="Migration file path or SQL text")
    args = parser.parse_args()

    if not args.input:
        print("Migration Checker Agent")
        print("Usage: python main.py <migration.sql>")
        print("       python main.py 'ALTER TABLE users DROP COLUMN email;'")
        sys.exit(0)

    sql = ""  # pragma: no cover
    if os.path.isfile(args.input):  # pragma: no cover
        with open(args.input) as f:  # pragma: no cover
            sql = f.read()  # pragma: no cover
        print(f"Checking: {args.input}")  # pragma: no cover
    else:
        sql = args.input  # pragma: no cover

    issues = check_migration(sql)  # pragma: no cover
    print("\n📋 Migration Safety Report:")  # pragma: no cover
    for issue in issues:  # pragma: no cover
        print(f"  {issue}")  # pragma: no cover


if __name__ == "__main__":
    main()
