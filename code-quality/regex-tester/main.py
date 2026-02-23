#!/usr/bin/env python3
"""CLI for Regex Tester."""
import argparse
import sys
import os
import json

sys.path.append(os.path.dirname(__file__))

from agent.tester import (
    run_regex_test, validate_pattern, batch_test, explain_pattern,
    format_result_markdown, COMMON_PATTERNS,
)


def cmd_test(args):
    """Test a regex pattern against input text."""
    text = args.text
    if args.file:
        with open(args.file, "r") as f:
            text = f.read()

    result = run_regex_test(args.pattern, text, flags=args.flags or "")

    if args.markdown:
        print(format_result_markdown(result))
    elif args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        if not result.is_valid:
            print(f"❌ Invalid regex: {result.error}", file=sys.stderr)
            sys.exit(1)

        print(f"Pattern: {result.pattern}")
        print(f"Matches: {result.match_count}\n")

        for i, m in enumerate(result.matches, 1):
            print(f"  {i}. '{m.match}' (pos {m.start}-{m.end})")
            if m.groups:
                print(f"     Groups: {m.groups}")

        if result.match_count == 0:
            print("  No matches found.")


def cmd_validate(args):
    """Validate a regex pattern."""
    info = validate_pattern(args.pattern)
    if info["valid"]:
        print(f"✅ Valid regex: {args.pattern}")
        print(f"   Named groups: {info['group_names'] or 'none'}")
        print(f"   Capture groups: {info['groups']}")
    else:
        print(f"❌ Invalid regex: {info['error']}")


def cmd_explain(args):
    """Explain a regex pattern."""
    parts = explain_pattern(args.pattern)
    print(f"Pattern: {args.pattern}\n")
    for part in parts:
        print(f"  {part}")


def cmd_library(args):
    """Show common regex patterns."""
    if args.name:
        pattern = COMMON_PATTERNS.get(args.name)
        if pattern:
            print(f"{args.name}: {pattern}")
        else:
            print(f"Pattern '{args.name}' not found. Use 'library' to see all.")
    else:
        print(f"{'Name':<20} Pattern")
        print("-" * 60)
        for name, pattern in sorted(COMMON_PATTERNS.items()):
            p = pattern[:38] + "..." if len(pattern) > 40 else pattern
            print(f"{name:<20} {p}")
        print(f"\n{len(COMMON_PATTERNS)} patterns available")


def cmd_extract(args):
    """Extract matches using a common pattern name."""
    pattern = COMMON_PATTERNS.get(args.name)
    if not pattern:
        print(f"Unknown pattern: {args.name}", file=sys.stderr)
        sys.exit(1)

    text = args.text
    if args.file:
        with open(args.file, "r") as f:
            text = f.read()

    result = run_regex_test(pattern, text)
    for m in result.matches:
        print(m.match)


def main():
    parser = argparse.ArgumentParser(description="Regex Tester — Test, validate, and explore regex patterns")
    sub = parser.add_subparsers(dest="command", required=True)

    # test
    p = sub.add_parser("test", help="Test a pattern against text")
    p.add_argument("pattern", help="Regex pattern")
    p.add_argument("text", nargs="?", default="", help="Input text")
    p.add_argument("--file", help="Read text from file")
    p.add_argument("--flags", help="Regex flags (i=ignorecase, m=multiline, s=dotall)")
    p.add_argument("--markdown", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_test)

    # validate
    p = sub.add_parser("validate", help="Validate a regex pattern")
    p.add_argument("pattern")
    p.set_defaults(func=cmd_validate)

    # explain
    p = sub.add_parser("explain", help="Explain regex components")
    p.add_argument("pattern")
    p.set_defaults(func=cmd_explain)

    # library
    p = sub.add_parser("library", help="Show common patterns")
    p.add_argument("name", nargs="?", help="Pattern name")
    p.set_defaults(func=cmd_library)

    # extract
    p = sub.add_parser("extract", help="Extract using a common pattern")
    p.add_argument("name", help="Pattern name (e.g. email, url, ipv4)")
    p.add_argument("text", nargs="?", default="")
    p.add_argument("--file", help="Read from file")
    p.set_defaults(func=cmd_extract)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
