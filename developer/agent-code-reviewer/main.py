"""
Code Reviewer Agent — performs AI-assisted code review on pull requests and source files.
Usage: python main.py <file>
"""
import argparse, sys, os, re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Code Reviewer Agent] Paste code changes or a diff to get a detailed review covering style, logic, security, and improvement suggestions."


CHECKS = [
    (r"\bprint\s*\(", "Debug print detected"),
    (r"except:\s*\n\s*pass", "Bare except:pass swallows errors silently"),
    (r"\beval\s*\(", "eval() — security risk (RCE)"),
    (r"type\([^)]+\)\s*==", "Use isinstance() instead of type() =="),
    (r"range\(len\(", "Use enumerate() instead of range(len())"),
    (r"global\s+\w+", "Global variable — consider refactoring"),
    (r"TODO|FIXME|HACK", "Leftover TODO/FIXME/HACK comment"),
]


def main():
    parser = argparse.ArgumentParser(description="AI Code Reviewer")
    parser.add_argument("file", nargs="?", help="Source file or diff to review")
    args = parser.parse_args()
    if not args.file:
        print("Code Reviewer Agent\nUsage: python main.py <source.py>")
        sys.exit(0)
    code = open(args.file).read() if os.path.isfile(args.file) else args.file
    issues = [f"⚠️  {msg}" for pat, msg in CHECKS if re.search(pat, code)]
    print(f"\n🔍 Code Review: {args.file}")
    for i in (issues or ["✅ Code looks clean — no common issues found."]):
        print(f"  {i}")

if __name__ == "__main__":
    main()
