#!/usr/bin/env python3
"""I18N Translator Agent — CLI entry point."""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from src.agent import I18nTranslatorAgent
from src.utils import console, print_header, print_step, print_success, print_error


def main():
    print_header("I18N Translator Agent")

    parser = argparse.ArgumentParser(description="Translate i18n JSON files preserving context")
    parser.add_argument("file", help="Path to source i18n JSON file")
    parser.add_argument("--lang", "-l", required=True, help="Target language (e.g., 'Spanish', 'Japanese', 'id')")
    parser.add_argument("--source-lang", "-s", default="English", help="Source language (default: English)")
    parser.add_argument("--output", "-o", help="Output file path (default: <file>.<lang>.json)")
    parser.add_argument("--review", action="store_true", help="Run quality review after translation")
    args = parser.parse_args()

    try:
        with open(args.file, "r") as f:
            source_content = f.read()
            source_data = json.loads(source_content)
    except FileNotFoundError:
        print_error(f"File not found: {args.file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON: {e}")
        sys.exit(1)

    print_step(f"Translating {len(source_data)} keys to {args.lang}...")

    try:
        agent = I18nTranslatorAgent()
        translated = agent.translate(source_content, args.lang, args.source_lang)
    except Exception as e:
        print_error(f"Translation failed: {e}")
        sys.exit(1)

    print_success(f"Translated {len(translated)} keys.")

    # Preview
    preview = json.dumps(translated, indent=2, ensure_ascii=False)
    console.print(Panel(
        Syntax(preview[:2000], "json", theme="monokai"),
        title=f"Translation Preview ({args.lang})",
        border_style="green",
    ))

    # Quality review
    if args.review:
        print_step("Running quality review...")
        try:
            review = agent.review_quality(source_content, json.dumps(translated, ensure_ascii=False), args.source_lang, args.lang)
            console.print(f"\n[bold]Quality Score:[/bold] {review.get('quality_score', '?')}/10")
            issues = review.get("issues", [])
            if issues:
                table = Table(title="Issues Found", border_style="yellow")
                table.add_column("Key")
                table.add_column("Issue")
                table.add_column("Suggestion")
                for issue in issues:
                    table.add_row(issue.get("key", "?"), issue.get("issue", ""), issue.get("suggestion", ""))
                console.print(table)
            else:
                print_success("No quality issues found!")
        except Exception as e:
            print_error(f"Quality review failed: {e}")

    # Save
    output_path = args.output or args.file.replace(".json", f".{args.lang.lower()[:2]}.json")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(translated, f, indent=2, ensure_ascii=False)
        print_success(f"Saved to {output_path}")
    except IOError as e:
        print_error(f"Failed to save: {e}")


if __name__ == "__main__":
    main()
