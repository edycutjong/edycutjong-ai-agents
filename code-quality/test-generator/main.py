#!/usr/bin/env python3
"""CLI for Test Generator Agent.

Usage:
    python main.py generate path/to/source.py           # Generate tests
    python main.py generate path/to/ --recursive        # Scan directory
    python main.py generate src/utils.py --framework jest  # Use Jest
    python main.py analyze path/to/source.py            # Analyze coverage gaps
"""
import argparse
import sys
import os

sys.path.append(os.path.dirname(__file__))

from agent.generator import TestGenerator
from agent.analyzer import CoverageAnalyzer


def main():
    parser = argparse.ArgumentParser(
        description="Test Generator — AI-powered unit & integration test scaffolding.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate
    gen = subparsers.add_parser("generate", help="Generate tests for source files")
    gen.add_argument("path", help="Source file or directory")
    gen.add_argument("-o", "--output", help="Output directory (default: tests/)")
    gen.add_argument("--framework", choices=["pytest", "jest", "unittest"],
                     default="pytest", help="Test framework (default: pytest)")
    gen.add_argument("--recursive", "-r", action="store_true",
                     help="Scan directory recursively")
    gen.add_argument("--edge-cases", action="store_true",
                     help="Include edge case tests")
    gen.add_argument("--mocks", action="store_true",
                     help="Generate mock/stub code for dependencies")
    gen.add_argument("--dry-run", action="store_true",
                     help="Preview tests without writing files")

    # analyze
    analyze = subparsers.add_parser("analyze", help="Analyze coverage gaps")
    analyze.add_argument("path", help="Source file or directory")
    analyze.add_argument("--format", choices=["text", "json", "markdown"],
                         default="text", help="Output format")

    args = parser.parse_args()

    if args.command == "generate":
        _generate(args)
    elif args.command == "analyze":
        _analyze(args)


def _generate(args):
    if not os.path.exists(args.path):
        print(f"Error: '{args.path}' not found.", file=sys.stderr)
        sys.exit(1)

    generator = TestGenerator(framework=args.framework)

    # Collect source files
    if os.path.isdir(args.path):
        sources = generator.scan_directory(args.path, recursive=args.recursive)
    else:
        sources = [args.path]

    if not sources:
        print("No source files found.")
        return

    print(f"Found {len(sources)} source file(s).")
    output_dir = args.output or "tests"

    total = 0
    for src in sources:
        print(f"\n📝 Generating tests for {os.path.basename(src)}...")
        try:
            result = generator.generate(
                filepath=src,
                include_edge_cases=args.edge_cases,
                generate_mocks=args.mocks,
            )
            if args.dry_run:
                print(result.preview())
            else:
                out_path = result.save(output_dir)
                print(f"   ✅ Written to {out_path}")
                total += 1
        except Exception as e:
            print(f"   ❌ Failed: {e}")

    if not args.dry_run:
        print(f"\n🎉 Generated {total}/{len(sources)} test file(s) in {output_dir}/")
    else:
        print(f"\n📋 Dry run complete — {len(sources)} file(s) previewed.")


def _analyze(args):
    if not os.path.exists(args.path):
        print(f"Error: '{args.path}' not found.", file=sys.stderr)
        sys.exit(1)

    analyzer = CoverageAnalyzer()
    report = analyzer.analyze(args.path)

    if args.format == "json":
        import json
        print(json.dumps(report.to_dict(), indent=2))
    elif args.format == "markdown":
        print(report.to_markdown())
    else:
        print(f"\nCoverage Analysis: {args.path}")
        print(f"  Functions found: {report.total_functions}")
        print(f"  With tests: {report.tested_functions}")
        print(f"  Missing tests: {report.untested_functions}")
        print(f"  Coverage: {report.coverage_percent:.1f}%")
        if report.suggestions:
            print(f"\nSuggested tests:")
            for s in report.suggestions:
                print(f"  • {s}")


if __name__ == "__main__":
    main()
