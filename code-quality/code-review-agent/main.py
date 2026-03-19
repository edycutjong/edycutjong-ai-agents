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
        try:  # pragma: no cover
            with open(args.file, "r") as f:  # pragma: no cover
                code = f.read()  # pragma: no cover
        except FileNotFoundError:  # pragma: no cover
            print_error(f"File not found: {args.file}")  # pragma: no cover
            sys.exit(1)  # pragma: no cover
    else:
        code = Prompt.ask("[bold cyan]Paste code to review[/bold cyan]")

    if not code.strip():
        print_error("No code provided.")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print_step("Reviewing code with Gemini...")

    try:
        agent = CodeReviewAgent()
        result = agent.review(code)
    except Exception as e:
        print_error(f"Review failed: {e}")
        sys.exit(1)

    print_success("Review complete!")  # pragma: no cover

    # Style issues
    if result.get("style_issues"):  # pragma: no cover
        table = Table(title="Style Issues", border_style="yellow")  # pragma: no cover
        table.add_column("Line", style="bold")  # pragma: no cover
        table.add_column("Issue")  # pragma: no cover
        table.add_column("Suggestion")  # pragma: no cover
        for issue in result["style_issues"]:  # pragma: no cover
            table.add_row(str(issue.get("line", "?")), issue.get("issue", ""), issue.get("suggestion", ""))  # pragma: no cover
        console.print(table)  # pragma: no cover

    # Bugs
    if result.get("bugs"):  # pragma: no cover
        table = Table(title="Bugs Found", border_style="red")  # pragma: no cover
        table.add_column("Line", style="bold")  # pragma: no cover
        table.add_column("Description")  # pragma: no cover
        table.add_column("Severity")  # pragma: no cover
        for bug in result["bugs"]:  # pragma: no cover
            table.add_row(str(bug.get("line", "?")), bug.get("description", ""), bug.get("severity", ""))  # pragma: no cover
        console.print(table)  # pragma: no cover

    # Security
    if result.get("security_issues"):  # pragma: no cover
        table = Table(title="Security Issues", border_style="red bold")  # pragma: no cover
        table.add_column("Line", style="bold")  # pragma: no cover
        table.add_column("Vulnerability")  # pragma: no cover
        table.add_column("Recommendation")  # pragma: no cover
        for issue in result["security_issues"]:  # pragma: no cover
            table.add_row(str(issue.get("line", "?")), issue.get("vulnerability", ""), issue.get("recommendation", ""))  # pragma: no cover
        console.print(table)  # pragma: no cover

    # Summary
    console.print(f"\n[bold]Quality:[/bold] {result.get('overall_quality', '?')}/10  |  [bold]Complexity:[/bold] {result.get('complexity_rating', '?')}/10")  # pragma: no cover
    console.print(f"[bold]Summary:[/bold] {result.get('summary', 'N/A')}")  # pragma: no cover


if __name__ == "__main__":
    main()
