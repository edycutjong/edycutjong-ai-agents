"""
AI Code Review Agent — reviews code changes for quality, bugs, and style.
Usage: python main.py <file>
"""
import argparse
import sys
import os
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[AI Code Review] Ready.\n\nPaste your code to get a detailed AI review covering code quality, potential bugs, style issues, and improvement suggestions."


CHECKS = [
    (r"\bprint\s*\(", "Debug print statement detected"),
    (r"except:\s*\n\s*pass", "Bare except:pass — swallows all errors silently"),
    (r"global\s+\w+", "Global variable usage — consider refactoring"),
    (r"\beval\s*\(", "eval() usage — security risk"),
    (r"type\([^)]+\)\s*==", "Use isinstance() instead of type() =="),
    (r"[^!]==['\"]True['\"]|[^!]==['\"]False['\"]", "String comparison to boolean"),
    (r"len\(\w+\)\s*==\s*0", "Use 'not collection' instead of len() == 0"),
    (r"range\(len\(", "Use enumerate() instead of range(len())"),
]


def review_code(code: str) -> list:
    issues = []
    for pattern, msg in CHECKS:
        if re.search(pattern, code):
            issues.append(f"⚠️  {msg}")
    if not issues:
        issues.append("✅ No common issues found.")
    return issues


def main():
    parser = argparse.ArgumentParser(description="Review code for quality and best practices")
    parser.add_argument("file", nargs="?", help="Source file to review")
    args = parser.parse_args()

    if not args.file:
        print("AI Code Review Agent")
        print("Usage: python main.py <source_file.py>")
        sys.exit(0)

    if not os.path.isfile(args.file):
        code = args.file
    else:
        with open(args.file) as f:
            code = f.read()

    issues = review_code(code)
    print(f"\n🔍 Code Review: {args.file if os.path.isfile(args.file) else '(inline)'}")
    for issue in issues:
        print(f"  {issue}")


if __name__ == "__main__":
    main()
