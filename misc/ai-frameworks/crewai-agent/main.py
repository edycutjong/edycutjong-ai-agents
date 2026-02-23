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
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set.")
        print("   Copy .env.example to .env and add your key.")
        return

    # Display header
    print(f"\n{'='*60}")
    print(f"🤖 CrewAI Research Agent")
    print(f"📚 Topic: {args.topic}")
    print(f"👥 Agents: Researcher → Writer → Editor")
    print(f"{'='*60}\n")

    print("🔄 Starting research crew...\n")

    try:
        # Run the crew
        report = run_crew(args.topic, verbose=args.verbose)

        # Display report
        print(f"\n{'─'*60}")
        print(f"📄 Final Report:\n")
        print(report)
        print(f"\n{'─'*60}")

        # Save report
        if not args.no_save:
            filepath = save_report(report, args.topic)
            print(f"\n💾 Report saved to: {filepath}")

        print("\n✅ Done!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
