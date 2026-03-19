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

    try:  # pragma: no cover
        with open(args.file, "r") as f:  # pragma: no cover
            source_content = f.read()  # pragma: no cover
            source_data = json.loads(source_content)  # pragma: no cover
    except FileNotFoundError:  # pragma: no cover
        print_error(f"File not found: {args.file}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover
    except json.JSONDecodeError as e:  # pragma: no cover
        print_error(f"Invalid JSON: {e}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print_step(f"Translating {len(source_data)} keys to {args.lang}...")  # pragma: no cover

    try:  # pragma: no cover
        agent = I18nTranslatorAgent()  # pragma: no cover
        translated = agent.translate(source_content, args.lang, args.source_lang)  # pragma: no cover
    except Exception as e:  # pragma: no cover
        print_error(f"Translation failed: {e}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print_success(f"Translated {len(translated)} keys.")  # pragma: no cover

    # Preview
    preview = json.dumps(translated, indent=2, ensure_ascii=False)  # pragma: no cover
    console.print(Panel(  # pragma: no cover
        Syntax(preview[:2000], "json", theme="monokai"),
        title=f"Translation Preview ({args.lang})",
        border_style="green",
    ))

    # Quality review
    if args.review:  # pragma: no cover
        print_step("Running quality review...")  # pragma: no cover
        try:  # pragma: no cover
            review = agent.review_quality(source_content, json.dumps(translated, ensure_ascii=False), args.source_lang, args.lang)  # pragma: no cover
            console.print(f"\n[bold]Quality Score:[/bold] {review.get('quality_score', '?')}/10")  # pragma: no cover
            issues = review.get("issues", [])  # pragma: no cover
            if issues:  # pragma: no cover
                table = Table(title="Issues Found", border_style="yellow")  # pragma: no cover
                table.add_column("Key")  # pragma: no cover
                table.add_column("Issue")  # pragma: no cover
                table.add_column("Suggestion")  # pragma: no cover
                for issue in issues:  # pragma: no cover
                    table.add_row(issue.get("key", "?"), issue.get("issue", ""), issue.get("suggestion", ""))  # pragma: no cover
                console.print(table)  # pragma: no cover
            else:
                print_success("No quality issues found!")  # pragma: no cover
        except Exception as e:  # pragma: no cover
            print_error(f"Quality review failed: {e}")  # pragma: no cover

    # Save
    output_path = args.output or args.file.replace(".json", f".{args.lang.lower()[:2]}.json")  # pragma: no cover
    try:  # pragma: no cover
        with open(output_path, "w", encoding="utf-8") as f:  # pragma: no cover
            json.dump(translated, f, indent=2, ensure_ascii=False)  # pragma: no cover
        print_success(f"Saved to {output_path}")  # pragma: no cover
    except IOError as e:  # pragma: no cover
        print_error(f"Failed to save: {e}")  # pragma: no cover


if __name__ == "__main__":
    main()
