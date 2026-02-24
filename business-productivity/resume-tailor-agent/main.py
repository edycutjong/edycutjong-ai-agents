#!/usr/bin/env python3
"""Resume Tailor Agent — CLI entry point."""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from src.agent import ResumeTailorAgent
from src.utils import console, print_header, print_step, print_success, print_error


def main():
    print_header("Resume Tailor Agent")

    parser = argparse.ArgumentParser(description="Tailor resume to match job descriptions")
    parser.add_argument("--resume", "-r", help="Path to resume file")
    parser.add_argument("--jd", "-j", help="Path to job description file")
    args = parser.parse_args()

    if args.resume:
        try:
            with open(args.resume, "r") as f:
                resume = f.read()
        except FileNotFoundError:
            print_error(f"Resume not found: {args.resume}")
            sys.exit(1)
    else:
        resume = Prompt.ask("[bold cyan]Paste your resume[/bold cyan]")

    if args.jd:
        try:
            with open(args.jd, "r") as f:
                jd = f.read()
        except FileNotFoundError:
            print_error(f"Job description not found: {args.jd}")
            sys.exit(1)
    else:
        jd = Prompt.ask("[bold cyan]Paste job description[/bold cyan]")

    if not resume.strip() or not jd.strip():
        print_error("Both resume and job description are required.")
        sys.exit(1)

    print_step("Analyzing with Gemini...")

    try:
        agent = ResumeTailorAgent()
        result = agent.tailor(resume, jd)
    except Exception as e:
        print_error(f"Analysis failed: {e}")
        sys.exit(1)

    print_success("Analysis complete!")

    # Scores
    console.print(f"\n[bold]ATS Score:[/bold] {result.get('ats_score', '?')}/100  |  [bold]Quality:[/bold] {result.get('quality_score', '?')}/10")
    console.print(Panel(result.get("summary", "N/A"), title="Summary", border_style="green"))

    # Keywords
    matched = result.get("matched_keywords", [])
    missing = result.get("missing_keywords", [])
    if matched or missing:
        console.print(f"\n[bold green]Matched Keywords:[/bold green] {', '.join(matched)}")
        console.print(f"[bold red]Missing Keywords:[/bold red] {', '.join(missing)}")

    # Suggestions
    suggestions = result.get("experience_suggestions", [])
    if suggestions:
        table = Table(title="Experience Improvements", border_style="cyan")
        table.add_column("Original", style="dim")
        table.add_column("Improved", style="bold green")
        for s in suggestions[:5]:
            table.add_row(s.get("original", ""), s.get("improved", ""))
        console.print(table)


if __name__ == "__main__":
    main()
