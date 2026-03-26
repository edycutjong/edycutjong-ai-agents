"""
Env File Auditor Agent — scans .env files for security issues and best practices.
Usage: python main.py <.env>
"""
import argparse
import os
import re
import sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Env File Auditor] Provide a .env file path to audit for security issues."


SENSITIVE_PATTERNS = [
    (r"(?i)(password|passwd|pwd)\s*=", "HARDCODED_PASSWORD", "Password in env file — use a secret manager"),
    (r"(?i)(secret|private.?key)\s*=", "SECRET_KEY", "Secret/private key detected — ensure not committed to git"),
    (r"(?i)(api.?key|apikey)\s*=\s*\S+", "API_KEY", "API key detected — verify .gitignore includes .env"),
    (r"(?i)(token)\s*=\s*\S+", "AUTH_TOKEN", "Auth token detected — rotate if exposed"),
    (r"(?i)(aws_access|aws_secret)", "AWS_CREDS", "AWS credentials — use IAM roles or AWS Vault instead"),
    (r"(?i)(database_url|db_url|mongo.*uri)\s*=", "DB_CONN", "Database connection string — verify encryption"),
]


def audit_env(content: str, filename: str = ".env") -> list:
    findings = []
    lines = content.splitlines()
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            findings.append({"line": i, "code": "INVALID_FORMAT",
                             "message": f"Invalid line (no '='): {stripped[:40]}", "severity": "WARNING"})
            continue
        key, _, value = stripped.partition("=")
        value = value.strip().strip("'\"")
        if not value:
            findings.append({"line": i, "code": "EMPTY_VALUE",
                             "message": f"{key.strip()} has no value", "severity": "INFO"})
        if value and value == value.upper() and len(value) > 20:
            pass  # Long uppercase values are likely real secrets
        for pattern, code, msg in SENSITIVE_PATTERNS:
            if re.search(pattern, stripped):
                findings.append({"line": i, "code": code, "message": msg, "severity": "HIGH"})
                break
        if " " in key.strip():
            findings.append({"line": i, "code": "SPACE_IN_KEY",
                             "message": f"Space in key name: '{key.strip()}'", "severity": "WARNING"})
    # Check for .gitignore
    env_dir = os.path.dirname(os.path.abspath(filename)) if os.path.exists(filename) else ""
    gitignore = os.path.join(env_dir, ".gitignore") if env_dir else ""
    if gitignore and os.path.isfile(gitignore):
        gi_content = open(gitignore).read()
        if ".env" not in gi_content:
            findings.append({"line": 0, "code": "NOT_GITIGNORED",
                             "message": ".env is not in .gitignore — risk of committing secrets",
                             "severity": "CRITICAL"})
    return findings


def format_report(findings: list) -> str:
    if not findings:
        return "✅ Env file looks clean — no issues found."
    lines = [f"🔐 Env Audit — {len(findings)} finding(s)\n"]
    icons = {"CRITICAL": "🔴", "HIGH": "🟠", "WARNING": "🟡", "INFO": "🔵"}
    for f in findings:
        icon = icons.get(f["severity"], "⚪")
        loc = f"L{f['line']}" if f["line"] else "General"
        lines.append(f"  {icon} [{f['code']}] {loc}: {f['message']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Env File Auditor Agent")
    parser.add_argument("file", nargs="?", help=".env file to audit")
    args = parser.parse_args()
    if not args.file:
        print("Env File Auditor Agent\nUsage: python main.py <.env>")
        sys.exit(0)
    if not os.path.isfile(args.file):
        print(f"Error: {args.file} not found")
        sys.exit(1)
    content = open(args.file).read()
    findings = audit_env(content, args.file)
    print(format_report(findings))


if __name__ == "__main__":  # pragma: no cover
    main()
