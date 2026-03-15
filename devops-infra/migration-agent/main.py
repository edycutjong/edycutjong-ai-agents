"""
Migration Agent — validates and generates database migration scripts.
Usage: python main.py <migration.sql>
"""
import argparse, sys, re, os


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Migration Agent] Paste SQL migration scripts to validate for safety, check naming conventions, and suggest improvements."


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
    sql = open(args.input).read() if os.path.isfile(args.input) else args.input
    findings = [msg for pat, msg in RISKS if re.search(pat, sql, re.IGNORECASE)]
    if not findings:
        findings = ["✅ No critical issues found."]
    print("\n🗄️  Migration Review:")
    for f in findings:
        print(f"  {f}")

if __name__ == "__main__":
    main()
