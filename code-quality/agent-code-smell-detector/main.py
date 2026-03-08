"""
Code Smell Detector — identifies code smells like long functions, deep nesting, magic numbers.
Usage: python main.py <source_file>
"""
import argparse
import sys
import os
import re
import ast


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Code Smell Detector] Ready.\n\nPaste code to detect smells: long functions, deep nesting, duplicated logic, magic numbers, and more."


def detect_smells(code: str, filename: str = "") -> list:
    smells = []
    lines = code.splitlines()

    # Magic numbers
    magic = re.findall(r'\b(?<!\.)\d{2,}\b(?!\s*[=,\]])', code)
    if len(magic) > 3:
        smells.append(f"🔢 Magic numbers detected ({len(magic)} occurrences) — use named constants.")

    # Long lines
    long_lines = [i+1 for i, l in enumerate(lines) if len(l) > 120]
    if long_lines:
        smells.append(f"📏 Long lines (>120 chars) at lines: {long_lines[:5]}")

    # Deep nesting (indentation > 4 levels = 16 spaces)
    deep = [i+1 for i, l in enumerate(lines) if len(l) - len(l.lstrip()) >= 16 and l.strip()]
    if deep:
        smells.append(f"🪆 Deep nesting (>4 levels) at lines: {deep[:5]}")

    # Long functions (>50 lines between def and next def)
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_lines = node.end_lineno - node.lineno
                if func_lines > 50:
                    smells.append(f"📦 Long function '{node.name}' ({func_lines} lines) — consider splitting.")
    except SyntaxError:
        pass

    if not smells:
        smells.append("✅ No obvious code smells detected.")

    return smells


def main():
    parser = argparse.ArgumentParser(description="Detect code smells in source files")
    parser.add_argument("file", nargs="?", help="Source file to analyze")
    args = parser.parse_args()

    if not args.file:
        print("Code Smell Detector")
        print("Usage: python main.py <source_file.py>")
        sys.exit(0)

    if not os.path.isfile(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)

    with open(args.file) as f:
        code = f.read()

    smells = detect_smells(code, args.file)
    print(f"\n👃 Code Smell Report: {args.file}")
    for smell in smells:
        print(f"  {smell}")


if __name__ == "__main__":
    main()
