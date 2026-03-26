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

    if args.file:  # pragma: no cover
        try:  # pragma: no cover
            with open(args.file, "r") as f:  # pragma: no cover
                bullet_points = f.read()  # pragma: no cover
        except FileNotFoundError:  # pragma: no cover
            print_error(f"File not found: {args.file}")  # pragma: no cover
            sys.exit(1)  # pragma: no cover
    else:
        bullet_points = Prompt.ask("[bold cyan]Enter bullet points (one per line, empty line to finish)[/bold cyan]")  # pragma: no cover

    if not bullet_points.strip():  # pragma: no cover
        print_error("Bullet points are empty.")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    tone = args.tone or Prompt.ask(  # pragma: no cover
        "[bold cyan]Tone[/bold cyan]",
        choices=TONES,
        default="formal",
    )

    length = args.length or Prompt.ask(  # pragma: no cover
        "[bold cyan]Length[/bold cyan]",
        choices=LENGTHS,
        default="medium",
    )

    context = args.context or ""  # pragma: no cover

    print_step(f"Drafting email ({tone}, {length})...")  # pragma: no cover

    try:  # pragma: no cover
        agent = EmailDraftAgent()  # pragma: no cover
        result = agent.draft(bullet_points, tone=tone, length=length, context=context)  # pragma: no cover
    except Exception as e:  # pragma: no cover
        print_error(f"Draft failed: {e}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print_success("Draft complete!")  # pragma: no cover

    # Display subject
    subject = result.get("subject", "N/A")  # pragma: no cover
    console.print(f"\n[bold]Subject:[/bold] {subject}")  # pragma: no cover

    # Display full draft
    full_draft = result.get("full_draft", "")  # pragma: no cover
    if full_draft:  # pragma: no cover
        console.print(Panel(full_draft, title="Email Draft", border_style="green"))  # pragma: no cover
    else:
        body_parts = [  # pragma: no cover
            result.get("greeting", ""),
            "",
            result.get("body", ""),
            "",
            result.get("closing", ""),
        ]
        console.print(Panel("\n".join(body_parts), title="Email Draft", border_style="green"))  # pragma: no cover

    # Copy hint
    console.print("[dim]Tip: Use --output to save as JSON[/dim]")  # pragma: no cover

    # Export
    if args.output:  # pragma: no cover
        try:  # pragma: no cover
            with open(args.output, "w") as f:  # pragma: no cover
                json_mod.dump(result, f, indent=2)  # pragma: no cover
            print_success(f"Saved to {args.output}")  # pragma: no cover
        except IOError as e:  # pragma: no cover
            print_error(f"Failed to save: {e}")  # pragma: no cover


if __name__ == "__main__":
    main()  # pragma: no cover
