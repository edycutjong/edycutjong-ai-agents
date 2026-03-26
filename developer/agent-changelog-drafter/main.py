"""
Changelog Drafter Agent — reads git commits and drafts a structured changelog.
Usage: python main.py [--since TAG] [--version VERSION]
"""
import argparse
import subprocess
import sys
import re
from datetime import date


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Changelog Drafter] Provide git log output or commit messages to draft a structured changelog."


CONV_COMMIT = re.compile(r"^(?:[\da-f]+ )?(\w+)(?:\(([^)]+)\))?!?:\s*(.+)", re.IGNORECASE)

CATEGORIES = {
    "feat": "Features", "fix": "Bug Fixes", "perf": "Performance",
    "refactor": "Refactoring", "docs": "Documentation", "test": "Tests",
    "ci": "CI/CD", "chore": "Chores", "style": "Styles",
    "build": "Build", "security": "Security",
}


def parse_commits(log: str) -> dict:
    sections = {}
    for line in log.strip().splitlines():
        m = CONV_COMMIT.match(line.strip())
        if m:
            ctype, scope, msg = m.group(1).lower(), m.group(2), m.group(3)
            cat = CATEGORIES.get(ctype, "Other")
        else:
            cat, scope, msg = "Other", None, line.strip()
        sections.setdefault(cat, []).append({"scope": scope, "message": msg})
    return sections


def format_changelog(version: str, sections: dict) -> str:
    today = date.today().isoformat()
    lines = [f"## [{version}] - {today}\n"]
    for cat in ["Features", "Bug Fixes", "Performance", "Security", "Refactoring",
                "Documentation", "Tests", "CI/CD", "Build", "Styles", "Chores", "Other"]:
        items = sections.get(cat, [])
        if not items:
            continue
        lines.append(f"\n### {cat}\n")
        for item in items:
            scope = f"**{item['scope']}:** " if item["scope"] else ""
            lines.append(f"- {scope}{item['message']}")
    return "\n".join(lines)


def get_git_log(since: str = "") -> str:
    cmd = ["git", "log", "--oneline", "--no-merges"]
    if since:
        cmd += [f"{since}..HEAD"]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def main():
    parser = argparse.ArgumentParser(description="Changelog Drafter Agent")
    parser.add_argument("--since", default="", help="Start tag/commit")
    parser.add_argument("--version", default="Unreleased", help="Version label")
    args = parser.parse_args()
    log = get_git_log(args.since)
    if not log:
        print("No commits found.")
        sys.exit(1)
    sections = parse_commits(log)
    print(format_changelog(args.version, sections))


if __name__ == "__main__":  # pragma: no cover
    main()
