#!/usr/bin/env python3
"""Docs QA Agent — CLI entry point."""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.panel import Panel
from src.agent import DocsQAAgent
from src.utils import console, print_header, print_step, print_success, print_error


def main():
    print_header("Docs QA Agent")

    parser = argparse.ArgumentParser(description="Answer questions about project documentation")
    parser.add_argument("path", help="Path to documentation file or directory")
    parser.add_argument("--question", "-q", help="Question to ask (interactive if omitted)")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print_error(f"Path not found: {args.path}")
        sys.exit(1)

    print_step(f"Ingesting documentation from {args.path}...")

    agent = DocsQAAgent()
    docs_content = agent.ingest_docs(args.path)

    if not docs_content.strip():
        print_error("No documentation files found (.md, .txt, .rst).")
        sys.exit(1)

    print_success(f"Documentation loaded ({len(docs_content)} characters).")

    question = args.question or Prompt.ask("[bold cyan]Your question[/bold cyan]")

    if not question.strip():
        print_error("No question provided.")
        sys.exit(1)

    print_step("Querying Gemini...")

    try:
        result = agent.ask(docs_content, question)
    except Exception as e:
        print_error(f"Query failed: {e}")
        sys.exit(1)

    # Display answer
    console.print(Panel(
        Markdown(result.get("answer", "No answer")),
        title="Answer",
        border_style="green",
    ))
    console.print(f"[bold]Confidence:[/bold] {result.get('confidence', '?')}")
    console.print(f"[bold]Sources:[/bold] {', '.join(result.get('sources', []))}")

    follow_ups = result.get("follow_up_questions", [])
    if follow_ups:
        console.print("\n[bold]Follow-up Questions:[/bold]")
        for q in follow_ups:
            console.print(f"  • {q}")

    tasks = result.get("tasks", [])
    if tasks:
        console.print("\n[bold]Tasks:[/bold]")
        for t in tasks:
            console.print(f"  ☐ {t}")


if __name__ == "__main__":
    main()
