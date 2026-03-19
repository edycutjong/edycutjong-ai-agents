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

    if not commits:  # pragma: no cover
        print_error("No commits found in the specified range.")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print_success(f"Found {len(commits)} commits.")  # pragma: no cover
    formatted = format_commits_for_agent(commits)  # pragma: no cover

    print_step("Generating changelog with Gemini...")  # pragma: no cover

    try:  # pragma: no cover
        agent = ChangelogWriterAgent()  # pragma: no cover
        changelog = agent.generate(formatted)  # pragma: no cover
    except Exception as e:  # pragma: no cover
        print_error(f"Generation failed: {e}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    console.print(Panel(Markdown(changelog), title="Generated Changelog", border_style="green"))  # pragma: no cover

    try:  # pragma: no cover
        with open(args.output, "w") as f:  # pragma: no cover
            f.write(changelog)  # pragma: no cover
        print_success(f"Saved to {args.output}")  # pragma: no cover
    except IOError as e:  # pragma: no cover
        print_error(f"Failed to save: {e}")  # pragma: no cover


if __name__ == "__main__":
    main()
