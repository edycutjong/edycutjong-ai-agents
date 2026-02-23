#!/usr/bin/env python3
"""CLI interface for Meeting Notes Organizer.

Usage:
    python cli.py transcript.txt                  # Process from file
    python cli.py transcript.txt -o report.md     # Save to markdown
    echo "..." | python cli.py -                  # Read from stdin
    python cli.py --dry-run transcript.txt        # Test without API key
"""
import argparse
import sys
import os
import json

sys.path.append(os.path.dirname(__file__))

from config import Config
from agent.processor import MeetingProcessor
from agent.integrations import export_to_markdown, draft_followup_email


def read_transcript(source):
    """Read transcript from file path or stdin."""
    if source == "-":
        return sys.stdin.read()
    if not os.path.exists(source):
        print(f"Error: File '{source}' not found.", file=sys.stderr)
        sys.exit(1)
    with open(source, "r") as f:
        return f.read()


def dry_run(transcript):
    """Process without AI — uses template-based extraction."""
    # Simple heuristic: split lines, guess speakers from "Name:" patterns
    lines = transcript.strip().split("\n")
    speakers = set()
    action_items = []

    for line in lines:
        line = line.strip()
        if ":" in line:
            speaker = line.split(":")[0].strip()
            if speaker and len(speaker) < 40:
                speakers.add(speaker)

        lower = line.lower()
        if any(kw in lower for kw in ["todo", "action", "need to", "should", "will", "deadline"]):
            action_items.append({
                "task": line,
                "assignee": "Unassigned",
                "priority": "Medium",
                "due_date": None,
            })

    speaker_list = [
        {"name": s, "role": "Unknown", "topics": [], "talk_percentage": 100 // max(len(speakers), 1)}
        for s in sorted(speakers)
    ]

    return {
        "summary": f"Meeting with {len(speakers)} participant(s). {len(lines)} lines of transcript.",
        "action_items": action_items,
        "speakers": speaker_list,
        "email_draft": draft_followup_email(
            f"Meeting with {len(speakers)} participants",
            action_items,
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Meeting Notes Organizer — Process meeting transcripts with AI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python cli.py meeting.txt\n"
               "  python cli.py meeting.txt -o notes.md\n"
               '  echo "John: Ship v2 by Friday" | python cli.py -\n'
               "  python cli.py --dry-run meeting.txt\n",
    )
    parser.add_argument("source", help="Path to transcript file, or '-' for stdin")
    parser.add_argument("-o", "--output", help="Save output to markdown file")
    parser.add_argument("--dry-run", action="store_true",
                        help="Process without AI (template-based, no API key needed)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of markdown")
    parser.add_argument("--api-key", help="OpenAI API key (overrides .env)")

    args = parser.parse_args()

    # Read transcript
    transcript = read_transcript(args.source)
    if not transcript.strip():
        print("Error: Empty transcript.", file=sys.stderr)
        sys.exit(1)

    # Process
    if args.dry_run:
        result = dry_run(transcript)
    else:
        api_key = args.api_key or Config.OPENAI_API_KEY
        if not api_key:
            print("Error: No API key. Use --api-key, set OPENAI_API_KEY in .env, or use --dry-run.",
                  file=sys.stderr)
            sys.exit(1)

        processor = MeetingProcessor(api_key=api_key)
        result = processor.process_transcript(transcript)

        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)

    # Output
    if args.json:
        output = json.dumps(result, indent=2)
    else:
        output = export_to_markdown(result, transcript=transcript)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"✅ Saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
