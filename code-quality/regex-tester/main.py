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
    text = args.text  # pragma: no cover
    if args.file:  # pragma: no cover
        with open(args.file, "r") as f:  # pragma: no cover
            text = f.read()  # pragma: no cover

    result = run_regex_test(args.pattern, text, flags=args.flags or "")  # pragma: no cover

    if args.markdown:  # pragma: no cover
        print(format_result_markdown(result))  # pragma: no cover
    elif args.json:  # pragma: no cover
        print(json.dumps(result.to_dict(), indent=2))  # pragma: no cover
    else:
        if not result.is_valid:  # pragma: no cover
            print(f"❌ Invalid regex: {result.error}", file=sys.stderr)  # pragma: no cover
            sys.exit(1)  # pragma: no cover

        print(f"Pattern: {result.pattern}")  # pragma: no cover
        print(f"Matches: {result.match_count}\n")  # pragma: no cover

        for i, m in enumerate(result.matches, 1):  # pragma: no cover
            print(f"  {i}. '{m.match}' (pos {m.start}-{m.end})")  # pragma: no cover
            if m.groups:  # pragma: no cover
                print(f"     Groups: {m.groups}")  # pragma: no cover

        if result.match_count == 0:  # pragma: no cover
            print("  No matches found.")  # pragma: no cover


def cmd_validate(args):
    """Validate a regex pattern."""
    info = validate_pattern(args.pattern)  # pragma: no cover
    if info["valid"]:  # pragma: no cover
        print(f"✅ Valid regex: {args.pattern}")  # pragma: no cover
        print(f"   Named groups: {info['group_names'] or 'none'}")  # pragma: no cover
        print(f"   Capture groups: {info['groups']}")  # pragma: no cover
    else:
        print(f"❌ Invalid regex: {info['error']}")  # pragma: no cover


def cmd_explain(args):
    """Explain a regex pattern."""
    parts = explain_pattern(args.pattern)  # pragma: no cover
    print(f"Pattern: {args.pattern}\n")  # pragma: no cover
    for part in parts:  # pragma: no cover
        print(f"  {part}")  # pragma: no cover


def cmd_library(args):
    """Show common regex patterns."""
    if args.name:  # pragma: no cover
        pattern = COMMON_PATTERNS.get(args.name)  # pragma: no cover
        if pattern:  # pragma: no cover
            print(f"{args.name}: {pattern}")  # pragma: no cover
        else:
            print(f"Pattern '{args.name}' not found. Use 'library' to see all.")  # pragma: no cover
    else:
        print(f"{'Name':<20} Pattern")  # pragma: no cover
        print("-" * 60)  # pragma: no cover
        for name, pattern in sorted(COMMON_PATTERNS.items()):  # pragma: no cover
            p = pattern[:38] + "..." if len(pattern) > 40 else pattern  # pragma: no cover
            print(f"{name:<20} {p}")  # pragma: no cover
        print(f"\n{len(COMMON_PATTERNS)} patterns available")  # pragma: no cover


def cmd_extract(args):
    """Extract matches using a common pattern name."""
    pattern = COMMON_PATTERNS.get(args.name)  # pragma: no cover
    if not pattern:  # pragma: no cover
        print(f"Unknown pattern: {args.name}", file=sys.stderr)  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    text = args.text  # pragma: no cover
    if args.file:  # pragma: no cover
        with open(args.file, "r") as f:  # pragma: no cover
            text = f.read()  # pragma: no cover

    result = run_regex_test(pattern, text)  # pragma: no cover
    for m in result.matches:  # pragma: no cover
        print(m.match)  # pragma: no cover


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
