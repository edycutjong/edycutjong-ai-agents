"""
Changelog Agent — generates changelogs from git history or commit descriptions.
Usage: python main.py [--since v1.0] [--version v2.0]
"""
import argparse, sys, subprocess
from datetime import date


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Changelog Agent] Paste commit messages or a git log to generate a formatted CHANGELOG.md."


def main():
    parser = argparse.ArgumentParser(description="Generate CHANGELOG from git log")
    parser.add_argument("--since", default="", help="Start tag (e.g. v1.0.0)")
    parser.add_argument("--version", default="Unreleased", help="Release version label")
    args = parser.parse_args()
    cmd = ["git", "log", "--oneline", "--no-merges"]
    if args.since:
        cmd.append(f"{args.since}..HEAD")
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()
    except Exception as e:
        print(f"Git error: {e}\nUsage: python main.py [--since v1.0] [--version v2.0]")
        sys.exit(0)
    if not out:
        print("No commits found.")
        sys.exit(0)
    print(f"# Changelog\n\n## [{args.version}] - {date.today()}\n")
    for line in out.splitlines():
        print(f"- {line[8:].strip()}")

if __name__ == "__main__":
    main()
