"""CLI entry point for the CrewAI research agent system."""

import argparse  # pragma: no cover
import os  # pragma: no cover
from datetime import datetime  # pragma: no cover

from rich.console import Console  # pragma: no cover
from rich.panel import Panel  # pragma: no cover
from rich.markdown import Markdown  # pragma: no cover

from crew import run_crew  # pragma: no cover

console = Console()  # pragma: no cover


def save_report(report: str, topic: str) -> str:  # pragma: no cover
    """Save the report to a markdown file.

    Args:
        report: The markdown report content.
        topic: The original topic.

    Returns:
        Path to the saved file.
    """
    os.makedirs("reports", exist_ok=True)  # pragma: no cover
    slug = topic.lower().replace(" ", "_")[:30]  # pragma: no cover
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # pragma: no cover
    filename = f"reports/{slug}_{timestamp}.md"  # pragma: no cover

    with open(filename, "w") as f:  # pragma: no cover
        f.write(f"# {topic}\n\n")  # pragma: no cover
        f.write(f"_Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n")  # pragma: no cover
        f.write(report)  # pragma: no cover

    return filename  # pragma: no cover


def main() -> None:  # pragma: no cover
    """Parse CLI arguments and run the research crew."""
    parser = argparse.ArgumentParser(  # pragma: no cover
        description="CrewAI Research Agent — Generate comprehensive reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --topic "AI trends 2025"
  python cli.py --topic "market analysis" --verbose
  python cli.py --topic "renewable energy" --no-save
        """,
    )
    parser.add_argument("--topic", type=str, required=True, help="Research topic")  # pragma: no cover
    parser.add_argument("--verbose", action="store_true", help="Show agent reasoning")  # pragma: no cover
    parser.add_argument("--no-save", action="store_true", help="Don't save to file")  # pragma: no cover

    args = parser.parse_args()  # pragma: no cover

    # Validate API key
    if not os.getenv("OPENAI_API_KEY"):  # pragma: no cover
        console.print(  # pragma: no cover
            Panel(
                "[red]❌ OPENAI_API_KEY not set.[/red]\n\n"
                "Copy .env.example to .env and add your key.",
                title="Configuration Error",
            )
        )
        return  # pragma: no cover

    # Display header
    console.print(  # pragma: no cover
        Panel(
            f"[bold cyan]📚 Research Topic:[/bold cyan] {args.topic}\n"
            f"[dim]Agents: Researcher → Writer → Editor[/dim]",
            title="🤖 CrewAI Research Agent",
            border_style="cyan",
        )
    )

    # Run the crew
    console.print("\n[yellow]🔄 Starting research crew...[/yellow]\n")  # pragma: no cover

    try:  # pragma: no cover
        report = run_crew(args.topic, verbose=args.verbose)  # pragma: no cover

        # Display report
        console.print("\n")  # pragma: no cover
        console.print(Panel(Markdown(report), title="📄 Final Report", border_style="green"))  # pragma: no cover

        # Save report
        if not args.no_save:  # pragma: no cover
            filepath = save_report(report, args.topic)  # pragma: no cover
            console.print(f"\n[green]💾 Report saved to:[/green] {filepath}")  # pragma: no cover

        console.print("\n[bold green]✅ Done![/bold green]")  # pragma: no cover

    except Exception as e:  # pragma: no cover
        console.print(f"\n[red]❌ Error: {e}[/red]")  # pragma: no cover
        raise  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
