"""CLI entry point for the CrewAI research agent system."""

import argparse
import os
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from crew import run_crew

console = Console()


def save_report(report: str, topic: str) -> str:
    """Save the report to a markdown file.

    Args:
        report: The markdown report content.
        topic: The original topic.

    Returns:
        Path to the saved file.
    """
    os.makedirs("reports", exist_ok=True)
    slug = topic.lower().replace(" ", "_")[:30]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/{slug}_{timestamp}.md"

    with open(filename, "w") as f:
        f.write(f"# {topic}\n\n")
        f.write(f"_Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n")
        f.write(report)

    return filename


def main() -> None:
    """Parse CLI arguments and run the research crew."""
    parser = argparse.ArgumentParser(
        description="CrewAI Research Agent — Generate comprehensive reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --topic "AI trends 2025"
  python cli.py --topic "market analysis" --verbose
  python cli.py --topic "renewable energy" --no-save
        """,
    )
    parser.add_argument("--topic", type=str, required=True, help="Research topic")
    parser.add_argument("--verbose", action="store_true", help="Show agent reasoning")
    parser.add_argument("--no-save", action="store_true", help="Don't save to file")

    args = parser.parse_args()

    # Validate API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print(
            Panel(
                "[red]❌ OPENAI_API_KEY not set.[/red]\n\n"
                "Copy .env.example to .env and add your key.",
                title="Configuration Error",
            )
        )
        return

    # Display header
    console.print(
        Panel(
            f"[bold cyan]📚 Research Topic:[/bold cyan] {args.topic}\n"
            f"[dim]Agents: Researcher → Writer → Editor[/dim]",
            title="🤖 CrewAI Research Agent",
            border_style="cyan",
        )
    )

    # Run the crew
    console.print("\n[yellow]🔄 Starting research crew...[/yellow]\n")

    try:
        report = run_crew(args.topic, verbose=args.verbose)

        # Display report
        console.print("\n")
        console.print(Panel(Markdown(report), title="📄 Final Report", border_style="green"))

        # Save report
        if not args.no_save:
            filepath = save_report(report, args.topic)
            console.print(f"\n[green]💾 Report saved to:[/green] {filepath}")

        console.print("\n[bold green]✅ Done![/bold green]")

    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        raise


if __name__ == "__main__":
    main()
