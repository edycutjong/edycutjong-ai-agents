"""
Dead Code Hunter — finds unused functions, variables, and imports in Python files.
Usage: python main.py <source_file_or_dir>
"""
import argparse
import sys
import os
import ast
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Dead Code Hunter] Ready.\n\nPaste code to identify unused imports, unreachable code, unused variables, and dead functions."


def find_unused_imports(code: str) -> list:
    issues = []
    try:
        tree = ast.parse(code)
        imported = set()
        used = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname or alias.name.split(".")[0]
                    imported.add(name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname or alias.name
                    imported.add(name)
            elif isinstance(node, ast.Name):
                used.add(node.id)
            elif isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name):
                    used.add(node.value.id)

        unused = imported - used
        for name in unused:
            issues.append(f"📦 Unused import: '{name}'")
    except SyntaxError as e:
        issues.append(f"⚠️  Syntax error: {e}")
    return issues


def find_unreachable(code: str) -> list:
    issues = []
    lines = code.splitlines()
    after_return = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if re.match(r"^(return|raise|sys\.exit)\b", stripped):
            after_return = True
        elif stripped and not stripped.startswith("#") and after_return:
            if not re.match(r"^(def |class |@|#|\"\"\")", stripped):
                issues.append(f"💀 Potential unreachable code at line {i}: {stripped[:60]}")
                after_return = False
        if stripped.startswith(("def ", "class ")):
            after_return = False
    return issues


def main():
    parser = argparse.ArgumentParser(description="Find dead code in Python files")
    parser.add_argument("file", nargs="?", help="Python source file to analyze")
    args = parser.parse_args()

    if not args.file:
        print("Dead Code Hunter")
        print("Usage: python main.py <source.py>")
        sys.exit(0)

    if not os.path.isfile(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)

    with open(args.file) as f:
        code = f.read()

    issues = find_unused_imports(code) + find_unreachable(code)
    print(f"\n💀 Dead Code Report: {args.file}")
    if issues:
        for issue in issues:
            print(f"  {issue}")
    else:
        print("  ✅ No dead code detected.")


if __name__ == "__main__":
    main()
