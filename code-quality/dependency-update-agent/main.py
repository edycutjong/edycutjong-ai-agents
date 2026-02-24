#!/usr/bin/env python3
"""Dependency Update Agent — CLI entry point."""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.table import Table
from src.agent import DependencyUpdateAgent
from src.utils import console, print_header, print_step, print_success, print_error


def main():
    print_header("Dependency Update Agent")

    parser = argparse.ArgumentParser(description="Check and suggest safe dependency updates")
    parser.add_argument("file", help="Path to dependency file (requirements.txt, package.json, etc.)")
    args = parser.parse_args()

    try:
        with open(args.file, "r") as f:
            deps_content = f.read()
    except FileNotFoundError:
        print_error(f"File not found: {args.file}")
        sys.exit(1)

    if not deps_content.strip():
        print_error("Dependency file is empty.")
        sys.exit(1)

    print_step(f"Analyzing dependencies from {args.file}...")

    try:
        agent = DependencyUpdateAgent()
        result = agent.analyze(deps_content)
    except Exception as e:
        print_error(f"Analysis failed: {e}")
        sys.exit(1)

    print_success(f"Found {result.get('total_outdated', 0)} outdated dependencies.")

    updates = result.get("updates", [])
    if updates:
        table = Table(title="Dependency Updates", border_style="cyan")
        table.add_column("Package", style="bold")
        table.add_column("Current")
        table.add_column("Latest")
        table.add_column("Type")
        table.add_column("Risk")
        table.add_column("Breaking?")
        for u in updates:
            table.add_row(
                u.get("package", "?"),
                u.get("current_version", "?"),
                u.get("latest_version", "?"),
                u.get("update_type", "?"),
                u.get("risk_level", "?"),
                "⚠ Yes" if u.get("breaking_changes") else "No",
            )
        console.print(table)

    batch = result.get("batch_plan", [])
    if batch:
        console.print("\n[bold]Recommended Update Order:[/bold]")
        for i, step in enumerate(batch, 1):
            console.print(f"  {i}. {step}")

    console.print(f"\n[bold]Summary:[/bold] {result.get('summary', 'N/A')}")


if __name__ == "__main__":
    main()
