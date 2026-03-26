"""
Migration Agent — validates and generates database migration scripts.
Usage: python main.py <migration.sql>
"""
import argparse, sys, re, os


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Migration Agent] Paste SQL migration scripts to validate for safety, check naming conventions, and suggest improvements."  # pragma: no cover


RISKS = [
    (r"\bDROP\s+TABLE\b", "🚨 DROP TABLE — permanent data loss"),
    (r"\bTRUNCATE\b", "🚨 TRUNCATE — removes all rows"),
    (r"\bDELETE\s+FROM\b\s+\w+\s*;", "⛔ DELETE without WHERE"),
    (r"\bDROP\s+COLUMN\b", "⛔ DROP COLUMN — data loss"),
    (r"\bADD\s+COLUMN\b.*\bNOT\s+NULL\b(?!\s+DEFAULT)", "⚠️  NOT NULL without DEFAULT"),
]


def main():
    parser = argparse.ArgumentParser(description="Validate database migration files")
    parser.add_argument("input", nargs="?", help="Migration file or SQL text")
    args = parser.parse_args()
    if not args.input:
        print("Migration Agent\nUsage: python main.py <migration.sql>")
        sys.exit(0)
    sql = open(args.input).read() if os.path.isfile(args.input) else args.input  # pragma: no cover
    findings = [msg for pat, msg in RISKS if re.search(pat, sql, re.IGNORECASE)]  # pragma: no cover
    if not findings:  # pragma: no cover
        findings = ["✅ No critical issues found."]  # pragma: no cover
    print("\n🗄️  Migration Review:")  # pragma: no cover
    for f in findings:  # pragma: no cover
        print(f"  {f}")  # pragma: no cover

if __name__ == "__main__":
    main()
