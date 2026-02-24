#!/usr/bin/env python3
"""Meeting Notes Summarizer — CLI entry point."""
import argparse
import sys
import os
import json as json_mod

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from src.agent import MeetingSummarizerAgent
from src.utils import console, print_header, print_step, print_success, print_error


def main():
    print_header("Meeting Notes Summarizer")

    parser = argparse.ArgumentParser(description="Summarize meeting transcripts into action items")
    parser.add_argument("--file", "-f", help="Path to a transcript file")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r") as f:
                transcript = f.read()
        except FileNotFoundError:
            print_error(f"File not found: {args.file}")
            sys.exit(1)
    else:
        transcript = Prompt.ask("[bold cyan]Paste meeting transcript[/bold cyan]")

    if not transcript.strip():
        print_error("Transcript is empty.")
        sys.exit(1)

    print_step("Summarizing with Gemini...")

    try:
        agent = MeetingSummarizerAgent()
        result = agent.summarize(transcript)
    except Exception as e:
        print_error(f"Summarization failed: {e}")
        sys.exit(1)

    print_success("Summary complete!")

    # Display summary
    console.print(Panel(result.get("summary", "N/A"), title=result.get("title", "Meeting Summary"), border_style="green"))

    # Key points
    key_points = result.get("key_points", [])
    if key_points:
        console.print("\n[bold]Key Points:[/bold]")
        for p in key_points:
            console.print(f"  • {p}")

    # Action items
    actions = result.get("action_items", [])
    if actions:
        table = Table(title="Action Items", border_style="cyan")
        table.add_column("Task", style="bold")
        table.add_column("Assignee")
        table.add_column("Deadline")
        for a in actions:
            table.add_row(a.get("task", "?"), a.get("assignee", "?"), a.get("deadline", "TBD"))
        console.print(table)

    # Decisions
    decisions = result.get("decisions", [])
    if decisions:
        console.print("\n[bold]Decisions:[/bold]")
        for d in decisions:
            console.print(f"  ✓ {d}")

    # Export
    if args.output:
        try:
            with open(args.output, "w") as f:
                json_mod.dump(result, f, indent=2)
            print_success(f"Saved to {args.output}")
        except IOError as e:
            print_error(f"Failed to save: {e}")


if __name__ == "__main__":
    main()
