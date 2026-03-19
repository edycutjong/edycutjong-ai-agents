#!/usr/bin/env python3
"""Bug Report Triage Agent — CLI entry point."""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.prompt import Prompt
from rich.table import Table
from rich.json import JSON
from src.agent import BugTriageAgent
from src.utils import console, print_header, print_step, print_success, print_error


def main():
    print_header("Bug Report Triage Agent")

    parser = argparse.ArgumentParser(description="Auto-triage bug reports by severity")
    parser.add_argument("--file", "-f", help="Path to a text file containing the bug report")
    args = parser.parse_args()

    if args.file:
        try:  # pragma: no cover
            with open(args.file, "r") as f:  # pragma: no cover
                bug_report = f.read()  # pragma: no cover
        except FileNotFoundError:  # pragma: no cover
            print_error(f"File not found: {args.file}")  # pragma: no cover
            sys.exit(1)  # pragma: no cover
    else:
        bug_report = Prompt.ask("[bold cyan]Paste bug report[/bold cyan]")

    if not bug_report.strip():
        print_error("Bug report is empty.")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print_step("Analyzing bug report with Gemini...")

    try:
        agent = BugTriageAgent()
        result = agent.triage(bug_report)
    except Exception as e:
        print_error(f"Triage failed: {e}")
        sys.exit(1)

    print_success("Triage complete!")  # pragma: no cover

    table = Table(title="Triage Results", border_style="cyan")  # pragma: no cover
    table.add_column("Field", style="bold")  # pragma: no cover
    table.add_column("Value")  # pragma: no cover
    table.add_row("Severity", str(result.get("severity", "N/A")))  # pragma: no cover
    table.add_row("Component", str(result.get("component", "N/A")))  # pragma: no cover
    table.add_row("Duplicate?", str(result.get("is_duplicate", False)))  # pragma: no cover
    table.add_row("Priority", str(result.get("priority_score", "N/A")))  # pragma: no cover
    table.add_row("Assignee", str(result.get("suggested_assignee", "N/A")))  # pragma: no cover
    table.add_row("Labels", ", ".join(result.get("labels", [])))  # pragma: no cover
    table.add_row("Summary", str(result.get("summary", "N/A")))  # pragma: no cover
    console.print(table)  # pragma: no cover


if __name__ == "__main__":
    main()
