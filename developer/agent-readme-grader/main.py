"""
README Grader Agent — scores READMEs on completeness and suggests improvements.
Usage: python main.py <README.md>
"""
import argparse
import os
import re
import sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[README Grader] Provide a README file to score its quality and get improvement suggestions."


REQUIRED_SECTIONS = {
    "title": (r"^#\s+\S", 1, "Project title (H1 heading)"),
    "description": (r"(?i)##\s*(about|description|overview|what)", 1, "Description/Overview section"),
    "installation": (r"(?i)##\s*(install|setup|getting\s*started)", 1, "Installation/Setup instructions"),
    "usage": (r"(?i)##\s*(usage|how\s*to|example|quick\s*start)", 1, "Usage examples"),
    "api": (r"(?i)##\s*(api|reference|documentation|docs)", 0.5, "API reference"),
    "contributing": (r"(?i)(contribut|CONTRIBUTING\.md)", 0.5, "Contributing guidelines"),
    "license": (r"(?i)(license|LICENSE)", 1, "License information"),
    "badges": (r"!\[.*\]\(https?://.*(?:badge|shield|img\.shields)", 0.5, "Status badges"),
    "code_examples": (r"```\w*\n", 1, "Code examples"),
    "table_of_contents": (r"(?i)##?\s*(table\s*of\s*contents|toc|contents)", 0.5, "Table of contents"),
}


def grade_readme(content: str) -> dict:
    score = 0
    max_score = sum(v[1] for v in REQUIRED_SECTIONS.values())
    found = []
    missing = []

    for name, (pattern, weight, label) in REQUIRED_SECTIONS.items():
        if re.search(pattern, content, re.MULTILINE):
            score += weight
            found.append(label)
        else:
            missing.append({"section": label, "weight": weight})

    # Bonus checks
    word_count = len(content.split())
    if word_count > 200:
        score += 0.5
    if word_count > 500:
        score += 0.5

    # Normalize to 10-point scale
    normalized = min(round((score / max_score) * 10, 1), 10)
    grade = "A" if normalized >= 8 else "B" if normalized >= 6 else "C" if normalized >= 4 else "D" if normalized >= 2 else "F"

    return {
        "score": normalized, "grade": grade, "word_count": word_count,
        "found": found, "missing": missing, "raw_score": score, "max_score": max_score
    }


def format_report(result: dict) -> str:
    icons = {"A": "🌟", "B": "✅", "C": "⚠️", "D": "🟡", "F": "🔴"}
    lines = [f"📝 README Score: {result['score']}/10 — Grade: {icons.get(result['grade'], '')} {result['grade']}",
             f"   Words: {result['word_count']}\n"]
    if result["found"]:
        lines.append("   ✅ Present:")
        for f in result["found"]:
            lines.append(f"      - {f}")
    if result["missing"]:
        lines.append("\n   ❌ Missing (add these to improve score):")
        for m in result["missing"]:
            lines.append(f"      - {m['section']} (+{m['weight']} pts)")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="README Grader Agent")
    parser.add_argument("file", nargs="?", help="README file to grade")
    args = parser.parse_args()
    if not args.file:
        print("README Grader Agent\nUsage: python main.py <README.md>")
        sys.exit(0)
    content = open(args.file).read()
    result = grade_readme(content)
    print(format_report(result))


if __name__ == "__main__":
    main()
