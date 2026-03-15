"""
Security Audit Agent — scans code and configs for security vulnerabilities.
Usage: python main.py <file_or_dir>
"""
import argparse, sys, os, re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Security Audit] Paste code, config files, or infrastructure definitions to get a security audit with CVE-style findings and remediation steps."


VULNS = [
    (r"eval\s*\(", "Critical", "eval() — Remote Code Execution risk"),
    (r"pickle\.loads\s*\(", "Critical", "pickle.loads() — Arbitrary code execution via deserialization"),
    (r"subprocess\.call\(.*shell\s*=\s*True", "High", "shell=True in subprocess — command injection"),
    (r"['\"]password['\"]:\s*['\"][^'\"]+['\"]", "High", "Hardcoded password in source code"),
    (r"SECRET(?:_KEY)?\s*=\s*['\"][^'\"]{4,}", "High", "Hardcoded secret/API key"),
    (r"cors\(\s*\{\s*origin\s*:\s*['\"]?\*", "Medium", "CORS wildcard (*) — allows all origins"),
    (r"md5\s*\(", "Medium", "MD5 used for hashing — use bcrypt/argon2 for passwords"),
    (r"allow_redirects\s*=\s*True", "Low", "Unvalidated redirect — check destination URL"),
    (r"verify\s*=\s*False", "Medium", "SSL verification disabled — MITM risk"),
    (r"DEBUG\s*=\s*True", "Low", "Debug mode enabled — disable in production"),
]


def main():
    parser = argparse.ArgumentParser(description="Security audit a source file or config")
    parser.add_argument("file", nargs="?", help="File to audit")
    args = parser.parse_args()
    if not args.file:
        print("Security Audit Agent\nUsage: python main.py <file>")
        sys.exit(0)
    code = open(args.file).read() if os.path.isfile(args.file) else args.file
    findings = [(sev, msg) for pat, sev, msg in VULNS if re.search(pat, code, re.IGNORECASE)]
    icons = {"Critical": "🚨", "High": "⛔", "Medium": "⚠️", "Low": "ℹ️"}
    print(f"\n🔐 Security Audit: {args.file}")
    if findings:
        for sev, msg in findings:
            print(f"  {icons[sev]} [{sev}] {msg}")
    else:
        print("  ✅ No obvious security issues found.")

if __name__ == "__main__":
    main()
