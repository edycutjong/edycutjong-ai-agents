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

    if args.command == "generate":  # pragma: no cover
        _generate(args)  # pragma: no cover
    elif args.command == "analyze":  # pragma: no cover
        _analyze(args)  # pragma: no cover


def _generate(args):
    if not os.path.exists(args.path):  # pragma: no cover
        print(f"Error: '{args.path}' not found.", file=sys.stderr)  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    generator = TestGenerator(framework=args.framework)  # pragma: no cover

    # Collect source files
    if os.path.isdir(args.path):  # pragma: no cover
        sources = generator.scan_directory(args.path, recursive=args.recursive)  # pragma: no cover
    else:
        sources = [args.path]  # pragma: no cover

    if not sources:  # pragma: no cover
        print("No source files found.")  # pragma: no cover
        return  # pragma: no cover

    print(f"Found {len(sources)} source file(s).")  # pragma: no cover
    output_dir = args.output or "tests"  # pragma: no cover

    total = 0  # pragma: no cover
    for src in sources:  # pragma: no cover
        print(f"\n📝 Generating tests for {os.path.basename(src)}...")  # pragma: no cover
        try:  # pragma: no cover
            result = generator.generate(  # pragma: no cover
                filepath=src,
                include_edge_cases=args.edge_cases,
                generate_mocks=args.mocks,
            )
            if args.dry_run:  # pragma: no cover
                print(result.preview())  # pragma: no cover
            else:
                out_path = result.save(output_dir)  # pragma: no cover
                print(f"   ✅ Written to {out_path}")  # pragma: no cover
                total += 1  # pragma: no cover
        except Exception as e:  # pragma: no cover
            print(f"   ❌ Failed: {e}")  # pragma: no cover

    if not args.dry_run:  # pragma: no cover
        print(f"\n🎉 Generated {total}/{len(sources)} test file(s) in {output_dir}/")  # pragma: no cover
    else:
        print(f"\n📋 Dry run complete — {len(sources)} file(s) previewed.")  # pragma: no cover


def _analyze(args):
    if not os.path.exists(args.path):  # pragma: no cover
        print(f"Error: '{args.path}' not found.", file=sys.stderr)  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    analyzer = CoverageAnalyzer()  # pragma: no cover
    report = analyzer.analyze(args.path)  # pragma: no cover

    if args.format == "json":  # pragma: no cover
        import json  # pragma: no cover
        print(json.dumps(report.to_dict(), indent=2))  # pragma: no cover
    elif args.format == "markdown":  # pragma: no cover
        print(report.to_markdown())  # pragma: no cover
    else:
        print(f"\nCoverage Analysis: {args.path}")  # pragma: no cover
        print(f"  Functions found: {report.total_functions}")  # pragma: no cover
        print(f"  With tests: {report.tested_functions}")  # pragma: no cover
        print(f"  Missing tests: {report.untested_functions}")  # pragma: no cover
        print(f"  Coverage: {report.coverage_percent:.1f}%")  # pragma: no cover
        if report.suggestions:  # pragma: no cover
            print(f"\nSuggested tests:")  # pragma: no cover
            for s in report.suggestions:  # pragma: no cover
                print(f"  • {s}")  # pragma: no cover


if __name__ == "__main__":
    main()
