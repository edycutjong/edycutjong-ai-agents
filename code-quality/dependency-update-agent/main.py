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

    try:  # pragma: no cover
        with open(args.file, "r") as f:  # pragma: no cover
            deps_content = f.read()  # pragma: no cover
    except FileNotFoundError:  # pragma: no cover
        print_error(f"File not found: {args.file}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    if not deps_content.strip():  # pragma: no cover
        print_error("Dependency file is empty.")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print_step(f"Analyzing dependencies from {args.file}...")  # pragma: no cover

    try:  # pragma: no cover
        agent = DependencyUpdateAgent()  # pragma: no cover
        result = agent.analyze(deps_content)  # pragma: no cover
    except Exception as e:  # pragma: no cover
        print_error(f"Analysis failed: {e}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print_success(f"Found {result.get('total_outdated', 0)} outdated dependencies.")  # pragma: no cover

    updates = result.get("updates", [])  # pragma: no cover
    if updates:  # pragma: no cover
        table = Table(title="Dependency Updates", border_style="cyan")  # pragma: no cover
        table.add_column("Package", style="bold")  # pragma: no cover
        table.add_column("Current")  # pragma: no cover
        table.add_column("Latest")  # pragma: no cover
        table.add_column("Type")  # pragma: no cover
        table.add_column("Risk")  # pragma: no cover
        table.add_column("Breaking?")  # pragma: no cover
        for u in updates:  # pragma: no cover
            table.add_row(  # pragma: no cover
                u.get("package", "?"),
                u.get("current_version", "?"),
                u.get("latest_version", "?"),
                u.get("update_type", "?"),
                u.get("risk_level", "?"),
                "⚠ Yes" if u.get("breaking_changes") else "No",
            )
        console.print(table)  # pragma: no cover

    batch = result.get("batch_plan", [])  # pragma: no cover
    if batch:  # pragma: no cover
        console.print("\n[bold]Recommended Update Order:[/bold]")  # pragma: no cover
        for i, step in enumerate(batch, 1):  # pragma: no cover
            console.print(f"  {i}. {step}")  # pragma: no cover

    console.print(f"\n[bold]Summary:[/bold] {result.get('summary', 'N/A')}")  # pragma: no cover


if __name__ == "__main__":
    main()
