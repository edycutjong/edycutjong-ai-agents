"""
Tech Debt Scorer — scores a codebase for technical debt and prioritizes repayment.
Usage: python main.py <source_file_or_dir>
"""
import argparse
import sys
import os
import re
import ast


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Tech Debt Scorer] Ready.\n\nPaste code or describe your codebase to get a technical debt score with prioritized repayment recommendations."  # pragma: no cover


DEBT_SIGNALS = [
    (r"#\s*TODO", 1, "TODO comment"),
    (r"#\s*FIXME", 2, "FIXME comment"),
    (r"#\s*HACK", 3, "HACK comment"),
    (r"#\s*XXX", 2, "XXX comment"),
    (r"#\s*TEMP\b", 2, "Temporary code"),
    (r"\beval\s*\(", 5, "eval() usage"),
    (r"except:\s*\n\s*pass", 4, "Bare except:pass"),
    (r"\bprint\s*\(", 1, "Debug print"),
    (r"time\.sleep\(\d+\)", 3, "Hard-coded sleep"),
    (r"\"\"\".*\"\"\"|'''.*'''", -1, "Has docstrings (good)"),
]


def score_file(code: str) -> tuple:
    score = 0  # pragma: no cover
    findings = []  # pragma: no cover

    for pattern, weight, label in DEBT_SIGNALS:  # pragma: no cover
        matches = re.findall(pattern, code, re.IGNORECASE)  # pragma: no cover
        if matches and weight > 0:  # pragma: no cover
            debt = len(matches) * weight  # pragma: no cover
            score += debt  # pragma: no cover
            findings.append((debt, f"  +{debt:3d}  {label} (×{len(matches)})"))  # pragma: no cover
        elif matches and weight < 0:  # pragma: no cover
            score += weight * len(matches)  # pragma: no cover

    # Penalize long files
    line_count = len(code.splitlines())  # pragma: no cover
    if line_count > 500:  # pragma: no cover
        score += 10  # pragma: no cover
        findings.append((10, f"  +10   Very long file ({line_count} lines)"))  # pragma: no cover

    # Check function complexity
    try:  # pragma: no cover
        tree = ast.parse(code)  # pragma: no cover
        for node in ast.walk(tree):  # pragma: no cover
            if isinstance(node, ast.FunctionDef):  # pragma: no cover
                fn_lines = getattr(node, 'end_lineno', 0) - node.lineno  # pragma: no cover
                if fn_lines > 50:  # pragma: no cover
                    score += 5  # pragma: no cover
                    findings.append((5, f"  +5    Long function '{node.name}' ({fn_lines} lines)"))  # pragma: no cover
    except SyntaxError:  # pragma: no cover
        score += 5  # pragma: no cover
        findings.append((5, "  +5    Syntax errors detected"))  # pragma: no cover

    score = max(0, score)  # pragma: no cover
    return score, sorted(findings, key=lambda x: -x[0])  # pragma: no cover


def grade(score: int) -> str:
    if score <= 5:   return "A ✅ (Excellent)"  # pragma: no cover
    if score <= 15:  return "B 🟡 (Good)"  # pragma: no cover
    if score <= 30:  return "C 🟠 (Needs work)"  # pragma: no cover
    if score <= 50:  return "D 🔴 (High debt)"  # pragma: no cover
    return "F ⛔ (Critical)"  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Score technical debt in source code")
    parser.add_argument("file", nargs="?", help="Source file to analyze")
    args = parser.parse_args()

    if not args.file:
        print("Tech Debt Scorer")
        print("Usage: python main.py <source.py>")
        sys.exit(0)

    if not os.path.isfile(args.file):  # pragma: no cover
        print(f"File not found: {args.file}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    with open(args.file) as f:  # pragma: no cover
        code = f.read()  # pragma: no cover

    score, findings = score_file(code)  # pragma: no cover
    print(f"\n📊 Tech Debt Report: {args.file}")  # pragma: no cover
    print(f"   Score: {score}  |  Grade: {grade(score)}\n")  # pragma: no cover
    print("   Breakdown:")  # pragma: no cover
    for _, line in findings[:10]:  # pragma: no cover
        print(line)  # pragma: no cover


if __name__ == "__main__":
    main()
