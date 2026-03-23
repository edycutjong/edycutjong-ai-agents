"""
PR Risk Scorer Agent — analyzes pull request diffs and assigns a composite risk score.
Usage: python main.py <diff_file>
"""
import argparse
import os
import re
import sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[PR Risk Scorer] Provide a PR diff to get a risk score and analysis."


RISK_SIGNALS = {
    "auth_changes": (r"(?i)(auth|login|token|session|password|jwt|oauth|apikey|secret)", 3),
    "db_migration": (r"(?i)(migration|alter\s+table|drop\s+table|create\s+table|add\s+column)", 3),
    "security_file": (r"(?i)(\.env|secret|credential|certificate|\.pem|\.key)", 4),
    "hardcoded_secret": (r"(?:password|secret|key|token)\s*=\s*['\"][^'\"]{8,}", 5),
    "large_file_change": (None, 2),
    "no_tests": (None, 2),
    "config_change": (r"(?i)(\.yml|\.yaml|\.json|\.toml|Dockerfile|nginx|\.conf)", 1),
    "dependency_change": (r"(?i)(package\.json|requirements\.txt|Cargo\.toml|go\.mod|Gemfile)", 2),
}


def analyze_diff(content: str) -> dict:
    lines = content.splitlines()
    total_lines = len(lines)
    added = sum(1 for l in lines if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in lines if l.startswith("-") and not l.startswith("---"))
    files_changed = set()
    for l in lines:
        m = re.match(r"^(?:diff --git a/.+ b/|[\+\-]{3} [ab]/)(.+)", l)
        if m:
            files_changed.add(m.group(1))

    signals = []
    score = 0

    # Size risk
    if added + removed > 500:
        signals.append({"signal": "LARGE_DIFF", "weight": 3, "detail": f"{added + removed} lines changed"})
        score += 3
    elif added + removed > 200:
        signals.append({"signal": "MEDIUM_DIFF", "weight": 1, "detail": f"{added + removed} lines changed"})
        score += 1

    # Pattern-based risks
    for name, (pattern, weight) in RISK_SIGNALS.items():
        if pattern and re.search(pattern, content):
            signals.append({"signal": name.upper(), "weight": weight, "detail": f"Pattern detected"})
            score += weight

    # No test files
    test_files = [f for f in files_changed if re.search(r"(?i)(test|spec)", f)]
    if not test_files and len(files_changed) > 2:
        signals.append({"signal": "NO_TESTS", "weight": 2, "detail": "No test files in PR"})
        score += 2

    risk_level = "LOW" if score <= 3 else "MEDIUM" if score <= 7 else "HIGH" if score <= 12 else "CRITICAL"
    return {
        "score": min(score, 10), "risk_level": risk_level,
        "files_changed": len(files_changed), "lines_added": added,
        "lines_removed": removed, "signals": signals
    }


def format_report(result: dict) -> str:
    icons = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}
    lines = [f"📊 PR Risk Score: {result['score']}/10 {icons.get(result['risk_level'], '⚪')} {result['risk_level']}",
             f"   Files: {result['files_changed']} | +{result['lines_added']} / -{result['lines_removed']}\n"]
    if result["signals"]:
        lines.append("   Risk signals:")
        for s in result["signals"]:
            lines.append(f"     ⚡ {s['signal']} (weight: {s['weight']}): {s['detail']}")
    else:
        lines.append("   ✅ No risk signals detected")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="PR Risk Scorer Agent")
    parser.add_argument("file", nargs="?", help="Diff file to analyze")
    args = parser.parse_args()
    if not args.file:
        print("PR Risk Scorer Agent\nUsage: python main.py <diff_file>")
        sys.exit(0)
    content = open(args.file).read()
    result = analyze_diff(content)
    print(format_report(result))


if __name__ == "__main__":
    main()
