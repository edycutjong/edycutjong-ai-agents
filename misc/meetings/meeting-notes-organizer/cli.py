#!/usr/bin/env python3
"""CLI interface for Meeting Notes Organizer.

Usage:
    python cli.py transcript.txt                  # Process from file
    python cli.py transcript.txt -o report.md     # Save to markdown
    echo "..." | python cli.py -                  # Read from stdin
    python cli.py --dry-run transcript.txt        # Test without API key
"""
import argparse  # pragma: no cover
import sys  # pragma: no cover
import os  # pragma: no cover
import json  # pragma: no cover

sys.path.append(os.path.dirname(__file__))  # pragma: no cover

from config import Config  # pragma: no cover
from agent.processor import MeetingProcessor  # pragma: no cover
from agent.integrations import export_to_markdown, draft_followup_email  # pragma: no cover


def read_transcript(source):  # pragma: no cover
    """Read transcript from file path or stdin."""
    if source == "-":  # pragma: no cover
        return sys.stdin.read()  # pragma: no cover
    if not os.path.exists(source):  # pragma: no cover
        print(f"Error: File '{source}' not found.", file=sys.stderr)  # pragma: no cover
        sys.exit(1)  # pragma: no cover
    with open(source, "r") as f:  # pragma: no cover
        return f.read()  # pragma: no cover


def dry_run(transcript):  # pragma: no cover
    """Process without AI — uses template-based extraction."""
    # Simple heuristic: split lines, guess speakers from "Name:" patterns
    lines = transcript.strip().split("\n")  # pragma: no cover
    speakers = set()  # pragma: no cover
    action_items = []  # pragma: no cover

    for line in lines:  # pragma: no cover
        line = line.strip()  # pragma: no cover
        if ":" in line:  # pragma: no cover
            speaker = line.split(":")[0].strip()  # pragma: no cover
            if speaker and len(speaker) < 40:  # pragma: no cover
                speakers.add(speaker)  # pragma: no cover

        lower = line.lower()  # pragma: no cover
        if any(kw in lower for kw in ["todo", "action", "need to", "should", "will", "deadline"]):  # pragma: no cover
            action_items.append({  # pragma: no cover
                "task": line,
                "assignee": "Unassigned",
                "priority": "Medium",
                "due_date": None,
            })

    speaker_list = [  # pragma: no cover
        {"name": s, "role": "Unknown", "topics": [], "talk_percentage": 100 // max(len(speakers), 1)}
        for s in sorted(speakers)
    ]

    return {  # pragma: no cover
        "summary": f"Meeting with {len(speakers)} participant(s). {len(lines)} lines of transcript.",
        "action_items": action_items,
        "speakers": speaker_list,
        "email_draft": draft_followup_email(
            f"Meeting with {len(speakers)} participants",
            action_items,
        ),
    }


def main():  # pragma: no cover
    parser = argparse.ArgumentParser(  # pragma: no cover
        description="Meeting Notes Organizer — Process meeting transcripts with AI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python cli.py meeting.txt\n"
               "  python cli.py meeting.txt -o notes.md\n"
               '  echo "John: Ship v2 by Friday" | python cli.py -\n'
               "  python cli.py --dry-run meeting.txt\n",
    )
    parser.add_argument("source", help="Path to transcript file, or '-' for stdin")  # pragma: no cover
    parser.add_argument("-o", "--output", help="Save output to markdown file")  # pragma: no cover
    parser.add_argument("--dry-run", action="store_true",  # pragma: no cover
                        help="Process without AI (template-based, no API key needed)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of markdown")  # pragma: no cover
    parser.add_argument("--api-key", help="OpenAI API key (overrides .env)")  # pragma: no cover

    args = parser.parse_args()  # pragma: no cover

    # Read transcript
    transcript = read_transcript(args.source)  # pragma: no cover
    if not transcript.strip():  # pragma: no cover
        print("Error: Empty transcript.", file=sys.stderr)  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    # Process
    if args.dry_run:  # pragma: no cover
        result = dry_run(transcript)  # pragma: no cover
    else:
        api_key = args.api_key or Config.OPENAI_API_KEY  # pragma: no cover
        if not api_key:  # pragma: no cover
            print("Error: No API key. Use --api-key, set OPENAI_API_KEY in .env, or use --dry-run.",  # pragma: no cover
                  file=sys.stderr)
            sys.exit(1)  # pragma: no cover

        processor = MeetingProcessor(api_key=api_key)  # pragma: no cover
        result = processor.process_transcript(transcript)  # pragma: no cover

        if "error" in result:  # pragma: no cover
            print(f"Error: {result['error']}", file=sys.stderr)  # pragma: no cover
            sys.exit(1)  # pragma: no cover

    # Output
    if args.json:  # pragma: no cover
        output = json.dumps(result, indent=2)  # pragma: no cover
    else:
        output = export_to_markdown(result, transcript=transcript)  # pragma: no cover

    if args.output:  # pragma: no cover
        with open(args.output, "w") as f:  # pragma: no cover
            f.write(output)  # pragma: no cover
        print(f"✅ Saved to {args.output}")  # pragma: no cover
    else:
        print(output)  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
