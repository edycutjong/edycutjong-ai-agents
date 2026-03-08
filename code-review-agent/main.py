"""
Code Review Agent — reviews code for bugs, style, and improvements.
Usage: python main.py <source_file>
"""
import argparse, sys, os, re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Code Review Agent] Paste your code to get a review covering bugs, style, security, and improvement suggestions."


CHECKS = [
    (r"\bprint\s*\(", "Debug print found"),
    (r"except:\s*\n\s*pass", "Bare except:pass swallows errors"),
    (r"\beval\s*\(", "eval() is a security risk"),
    (r"type\([^)]+\)\s*==", "Use isinstance() instead of type() =="),
    (r"range\(len\(", "Use enumerate() instead of range(len())"),
]


def main():
    parser = argparse.ArgumentParser(description="Code review tool")
    parser.add_argument("file", nargs="?", help="Source file to review")
    args = parser.parse_args()
    if not args.file:
        print("Code Review Agent\nUsage: python main.py <source.py>")
        sys.exit(0)
    code = open(args.file).read() if os.path.isfile(args.file) else args.file
    issues = [f"⚠️  {msg}" for pat, msg in CHECKS if re.search(pat, code)]
    print(f"\n🔍 Code Review: {args.file}")
    for i in (issues or ["✅ No obvious issues found."]):
        print(f"  {i}")

if __name__ == "__main__":
    main()
