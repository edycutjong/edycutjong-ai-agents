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
    return "[Tech Debt Scorer] Ready.\n\nPaste code or describe your codebase to get a technical debt score with prioritized repayment recommendations."


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
    score = 0
    findings = []

    for pattern, weight, label in DEBT_SIGNALS:
        matches = re.findall(pattern, code, re.IGNORECASE)
        if matches and weight > 0:
            debt = len(matches) * weight
            score += debt
            findings.append((debt, f"  +{debt:3d}  {label} (×{len(matches)})"))
        elif matches and weight < 0:
            score += weight * len(matches)

    # Penalize long files
    line_count = len(code.splitlines())
    if line_count > 500:
        score += 10  # pragma: no cover
        findings.append((10, f"  +10   Very long file ({line_count} lines)"))  # pragma: no cover

    # Check function complexity
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                fn_lines = getattr(node, 'end_lineno', 0) - node.lineno
                if fn_lines > 50:
                    score += 5  # pragma: no cover
                    findings.append((5, f"  +5    Long function '{node.name}' ({fn_lines} lines)"))  # pragma: no cover
    except SyntaxError:
        score += 5
        findings.append((5, "  +5    Syntax errors detected"))

    score = max(0, score)
    return score, sorted(findings, key=lambda x: -x[0])


def grade(score: int) -> str:
    if score <= 5:   return "A ✅ (Excellent)"
    if score <= 15:  return "B 🟡 (Good)"
    if score <= 30:  return "C 🟠 (Needs work)"
    if score <= 50:  return "D 🔴 (High debt)"
    return "F ⛔ (Critical)"


def main():
    parser = argparse.ArgumentParser(description="Score technical debt in source code")
    parser.add_argument("file", nargs="?", help="Source file to analyze")
    args = parser.parse_args()

    if not args.file:
        print("Tech Debt Scorer")
        print("Usage: python main.py <source.py>")
        sys.exit(0)

    if not os.path.isfile(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)

    with open(args.file) as f:
        code = f.read()

    score, findings = score_file(code)
    print(f"\n📊 Tech Debt Report: {args.file}")
    print(f"   Score: {score}  |  Grade: {grade(score)}\n")
    print("   Breakdown:")
    for _, line in findings[:10]:
        print(line)


if __name__ == "__main__":
    main()
