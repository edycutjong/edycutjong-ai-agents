#!/usr/bin/env python3
"""Changelog Writer Agent — CLI entry point."""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.panel import Panel
from src.agent import ChangelogWriterAgent
from src.git_utils import get_commits, format_commits_for_agent
from src.utils import console, print_header, print_step, print_success, print_error


def main():
    print_header("Changelog Writer Agent")

    parser = argparse.ArgumentParser(description="Generate changelogs from git commit history")
    parser.add_argument("--repo", "-r", default=".", help="Path to git repository (default: current dir)")
    parser.add_argument("--from", dest="from_ref", default="HEAD~10", help="Starting ref (default: HEAD~10)")
    parser.add_argument("--to", dest="to_ref", default="HEAD", help="Ending ref (default: HEAD)")
    parser.add_argument("--output", "-o", default="CHANGELOG.md", help="Output file (default: CHANGELOG.md)")
    args = parser.parse_args()

    print_step(f"Fetching commits from {args.from_ref}..{args.to_ref}...")

    try:
        commits = get_commits(args.repo, args.from_ref, args.to_ref)
    except Exception as e:
        print_error(f"Failed to read git log: {e}")
        sys.exit(1)

    if not commits:
        print_error("No commits found in the specified range.")
        sys.exit(1)

    print_success(f"Found {len(commits)} commits.")
    formatted = format_commits_for_agent(commits)

    print_step("Generating changelog with Gemini...")

    try:
        agent = ChangelogWriterAgent()
        changelog = agent.generate(formatted)
    except Exception as e:
        print_error(f"Generation failed: {e}")
        sys.exit(1)

    console.print(Panel(Markdown(changelog), title="Generated Changelog", border_style="green"))

    try:
        with open(args.output, "w") as f:
            f.write(changelog)
        print_success(f"Saved to {args.output}")
    except IOError as e:
        print_error(f"Failed to save: {e}")


if __name__ == "__main__":
    main()
