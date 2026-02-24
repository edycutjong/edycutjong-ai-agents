#!/usr/bin/env python3
"""Email Draft Agent — CLI entry point."""
import argparse
import sys
import os
import json as json_mod

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.prompt import Prompt
from rich.panel import Panel
from src.agent import EmailDraftAgent, TONES, LENGTHS
from src.utils import console, print_header, print_step, print_success, print_error


def main():
    print_header("Email Draft Agent")

    parser = argparse.ArgumentParser(description="Draft professional emails from bullet points")
    parser.add_argument("--file", "-f", help="Path to a file with bullet points")
    parser.add_argument("--tone", "-t", choices=TONES, default=None, help="Email tone")
    parser.add_argument("--length", "-l", choices=LENGTHS, default=None, help="Email length")
    parser.add_argument("--context", "-c", help="Thread context or previous email")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r") as f:
                bullet_points = f.read()
        except FileNotFoundError:
            print_error(f"File not found: {args.file}")
            sys.exit(1)
    else:
        bullet_points = Prompt.ask("[bold cyan]Enter bullet points (one per line, empty line to finish)[/bold cyan]")

    if not bullet_points.strip():
        print_error("Bullet points are empty.")
        sys.exit(1)

    tone = args.tone or Prompt.ask(
        "[bold cyan]Tone[/bold cyan]",
        choices=TONES,
        default="formal",
    )

    length = args.length or Prompt.ask(
        "[bold cyan]Length[/bold cyan]",
        choices=LENGTHS,
        default="medium",
    )

    context = args.context or ""

    print_step(f"Drafting email ({tone}, {length})...")

    try:
        agent = EmailDraftAgent()
        result = agent.draft(bullet_points, tone=tone, length=length, context=context)
    except Exception as e:
        print_error(f"Draft failed: {e}")
        sys.exit(1)

    print_success("Draft complete!")

    # Display subject
    subject = result.get("subject", "N/A")
    console.print(f"\n[bold]Subject:[/bold] {subject}")

    # Display full draft
    full_draft = result.get("full_draft", "")
    if full_draft:
        console.print(Panel(full_draft, title="Email Draft", border_style="green"))
    else:
        body_parts = [
            result.get("greeting", ""),
            "",
            result.get("body", ""),
            "",
            result.get("closing", ""),
        ]
        console.print(Panel("\n".join(body_parts), title="Email Draft", border_style="green"))

    # Copy hint
    console.print("[dim]Tip: Use --output to save as JSON[/dim]")

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
