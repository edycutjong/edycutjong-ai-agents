#!/usr/bin/env python3
"""Code Review Agent — CLI entry point."""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.prompt import Prompt
from rich.table import Table
from src.agent import CodeReviewAgent
from src.utils import console, print_header, print_step, print_success, print_error


def main():
    print_header("Code Review Agent")

    parser = argparse.ArgumentParser(description="Automated code review with AI")
    parser.add_argument("--file", "-f", help="Path to a source file to review")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r") as f:
                code = f.read()
        except FileNotFoundError:
            print_error(f"File not found: {args.file}")
            sys.exit(1)
    else:
        code = Prompt.ask("[bold cyan]Paste code to review[/bold cyan]")

    if not code.strip():
        print_error("No code provided.")
        sys.exit(1)

    print_step("Reviewing code with Gemini...")

    try:
        agent = CodeReviewAgent()
        result = agent.review(code)
    except Exception as e:
        print_error(f"Review failed: {e}")
        sys.exit(1)

    print_success("Review complete!")

    # Style issues
    if result.get("style_issues"):
        table = Table(title="Style Issues", border_style="yellow")
        table.add_column("Line", style="bold")
        table.add_column("Issue")
        table.add_column("Suggestion")
        for issue in result["style_issues"]:
            table.add_row(str(issue.get("line", "?")), issue.get("issue", ""), issue.get("suggestion", ""))
        console.print(table)

    # Bugs
    if result.get("bugs"):
        table = Table(title="Bugs Found", border_style="red")
        table.add_column("Line", style="bold")
        table.add_column("Description")
        table.add_column("Severity")
        for bug in result["bugs"]:
            table.add_row(str(bug.get("line", "?")), bug.get("description", ""), bug.get("severity", ""))
        console.print(table)

    # Security
    if result.get("security_issues"):
        table = Table(title="Security Issues", border_style="red bold")
        table.add_column("Line", style="bold")
        table.add_column("Vulnerability")
        table.add_column("Recommendation")
        for issue in result["security_issues"]:
            table.add_row(str(issue.get("line", "?")), issue.get("vulnerability", ""), issue.get("recommendation", ""))
        console.print(table)

    # Summary
    console.print(f"\n[bold]Quality:[/bold] {result.get('overall_quality', '?')}/10  |  [bold]Complexity:[/bold] {result.get('complexity_rating', '?')}/10")
    console.print(f"[bold]Summary:[/bold] {result.get('summary', 'N/A')}")


if __name__ == "__main__":
    main()
