"""CrewAI Research Agent — Main entry point.

A multi-agent crew that collaborates to research topics, write reports,
and generate insights using CrewAI for agent orchestration.

Usage:
    python main.py --topic "AI trends 2025"
    python main.py --topic "market analysis" --verbose
    python main.py --topic "renewable energy" --no-save
"""

import argparse
import os
from datetime import datetime

from crew import run_crew


def save_report(report: str, topic: str) -> str:
    """Save the generated report to a markdown file.

    Args:
        report: The markdown report content.
        topic: The original research topic.

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


def main() -> None:
    """Parse arguments and run the research crew."""
    parser = argparse.ArgumentParser(
        description="CrewAI Research Agent — Multi-agent report generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "AI trends 2025"
  python main.py --topic "market analysis" --verbose
  python main.py --topic "renewable energy" --no-save
        """,
    )
    parser.add_argument("--topic", type=str, required=True, help="Research topic")
    parser.add_argument("--verbose", action="store_true", help="Show agent reasoning")
    parser.add_argument("--no-save", action="store_true", help="Don't save report to file")

    args = parser.parse_args()

    # Validate API key
    if not os.getenv("OPENAI_API_KEY"):  # pragma: no cover
        print("❌ OPENAI_API_KEY not set.")  # pragma: no cover
        print("   Copy .env.example to .env and add your key.")  # pragma: no cover
        return  # pragma: no cover

    # Display header
    print(f"\n{'='*60}")  # pragma: no cover
    print(f"🤖 CrewAI Research Agent")  # pragma: no cover
    print(f"📚 Topic: {args.topic}")  # pragma: no cover
    print(f"👥 Agents: Researcher → Writer → Editor")  # pragma: no cover
    print(f"{'='*60}\n")  # pragma: no cover

    print("🔄 Starting research crew...\n")  # pragma: no cover

    try:  # pragma: no cover
        # Run the crew
        report = run_crew(args.topic, verbose=args.verbose)  # pragma: no cover

        # Display report
        print(f"\n{'─'*60}")  # pragma: no cover
        print(f"📄 Final Report:\n")  # pragma: no cover
        print(report)  # pragma: no cover
        print(f"\n{'─'*60}")  # pragma: no cover

        # Save report
        if not args.no_save:  # pragma: no cover
            filepath = save_report(report, args.topic)  # pragma: no cover
            print(f"\n💾 Report saved to: {filepath}")  # pragma: no cover

        print("\n✅ Done!")  # pragma: no cover

    except Exception as e:  # pragma: no cover
        print(f"\n❌ Error: {e}")  # pragma: no cover
        raise  # pragma: no cover


if __name__ == "__main__":
    main()
