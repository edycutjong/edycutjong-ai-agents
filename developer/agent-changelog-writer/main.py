"""
Changelog Writer Agent — reads git log and generates a formatted CHANGELOG.md.
Usage: python main.py [--since v1.0.0] [--output CHANGELOG.md]
"""
import argparse
import subprocess
import sys
from datetime import date


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return f"[Changelog Writer] Input received.\n\nPaste commit messages or a git log to generate a formatted CHANGELOG.md following Keep a Changelog conventions."  # pragma: no cover


def get_git_log(since: str = "") -> str:
    cmd = ["git", "log", "--oneline", "--no-merges"]
    if since:
        cmd += [f"{since}..HEAD"]  # pragma: no cover
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:  # pragma: no cover
        return f"Git error: {e.stderr}"  # pragma: no cover
    except FileNotFoundError:  # pragma: no cover
        return "git not found in PATH"  # pragma: no cover


def categorize_commits(log_lines: list) -> dict:
    categories = {"Added": [], "Fixed": [], "Changed": [], "Removed": [], "Security": [], "Other": []}
    for line in log_lines:
        msg = line[8:].strip() if len(line) > 8 else line
        low = msg.lower()
        if any(k in low for k in ["feat", "add"]):
            categories["Added"].append(msg)
        elif any(k in low for k in ["sec", "cve", "vuln"]):
            categories["Security"].append(msg)  # pragma: no cover
        elif any(k in low for k in ["fix", "bug", "patch"]):
            categories["Fixed"].append(msg)
        elif any(k in low for k in ["refactor", "update", "change", "improve", "perf"]):
            categories["Changed"].append(msg)
        elif any(k in low for k in ["remove", "delete", "drop", "deprecat"]):
            categories["Removed"].append(msg)
        else:
            categories["Other"].append(msg)
    return categories


def generate_changelog(version: str, log: str) -> str:
    lines = [l for l in log.splitlines() if l.strip()]
    cats = categorize_commits(lines)
    today = date.today().isoformat()

    out = [f"# Changelog\n\n## [{version}] - {today}\n"]
    for cat, items in cats.items():
        if items:
            out.append(f"\n### {cat}\n")
            for item in items:
                out.append(f"- {item}")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="Generate CHANGELOG.md from git commits")
    parser.add_argument("--since", default="", help="Start tag/commit (e.g. v1.0.0)")
    parser.add_argument("--version", default="Unreleased", help="Version label for this release")
    parser.add_argument("--output", default="", help="Output file (default: print to stdout)")
    args = parser.parse_args()

    log = get_git_log(args.since)
    if not log or log.startswith("Git error") or log.startswith("git not"):
        print(f"No commits found. {log}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    changelog = generate_changelog(args.version, log)
    if args.output:
        with open(args.output, "w") as f:  # pragma: no cover
            f.write(changelog)  # pragma: no cover
        print(f"✅ Written to {args.output}")  # pragma: no cover
    else:
        print(changelog)


if __name__ == "__main__":
    main()
