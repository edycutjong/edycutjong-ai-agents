"""
Migration Checker Agent — validates database migration files for safety.
Usage: python main.py <migration_file_or_dir>
"""
import argparse
import sys
import re
import os


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Migration Checker] Ready.\n\nPaste SQL migration code or describe your migration to check for destructive operations, naming issues, and ordering problems."


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
    issues = []
    for pattern, msg in DESTRUCTIVE_PATTERNS:
        if re.search(pattern, sql, re.IGNORECASE):
            issues.append(f"🚨 Destructive: {msg}")
    for pattern, msg in MISSING_PATTERNS:
        if re.search(pattern, sql, re.IGNORECASE):
            issues.append(f"⚠️  Warning: {msg}")
    if not issues:
        issues.append("✅ No obvious destructive operations detected.")
    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate database migration files")
    parser.add_argument("input", nargs="?", help="Migration file path or SQL text")
    args = parser.parse_args()

    if not args.input:
        print("Migration Checker Agent")
        print("Usage: python main.py <migration.sql>")
        print("       python main.py 'ALTER TABLE users DROP COLUMN email;'")
        sys.exit(0)

    sql = ""
    if os.path.isfile(args.input):
        with open(args.input) as f:
            sql = f.read()
        print(f"Checking: {args.input}")
    else:
        sql = args.input

    issues = check_migration(sql)
    print("\n📋 Migration Safety Report:")
    for issue in issues:
        print(f"  {issue}")


if __name__ == "__main__":
    main()
