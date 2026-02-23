import argparse
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

# Add current directory to path so we can import tools
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.scanner import Scanner
from tools.locales import LocaleManager
from tools.analyzer import Analyzer
from tools.translator import Translator

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Find missing i18n keys in your project.")
    parser.add_argument("--source", "-s", required=True, help="Path to source code directory.")
    parser.add_argument("--locale", "-l", required=True, help="Path to locale files directory.")
    parser.add_argument("--source-lang", default="en", help="Source language code (default: en).")
    parser.add_argument("--auto-translate", action="store_true", help="Auto-translate missing keys using OpenAI.")
    parser.add_argument("--fix", action="store_true", help="Apply fixes (add missing keys to locale files).")

    args = parser.parse_args()

    source_dir = args.source
    locale_dir = args.locale
    source_lang = args.source_lang

    console.print(Panel.fit("[bold blue]i18n Missing Key Finder[/bold blue]", border_style="blue"))

    if not os.path.exists(source_dir):
        console.print(f"[red]Error: Source directory '{source_dir}' does not exist.[/red]")
        sys.exit(1)

    if not os.path.exists(locale_dir):
        console.print(f"[red]Error: Locale directory '{locale_dir}' does not exist.[/red]")
        sys.exit(1)

    # 1. Scan Source Code
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task = progress.add_task(description="Scanning source code...", total=None)
        scanner = Scanner()
        source_keys = scanner.scan_directory(source_dir)
        progress.update(task, completed=True)

    console.print(f"[green]Found {len(source_keys)} keys in source code.[/green]")

    # 2. Load Locales
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task = progress.add_task(description="Loading locale files...", total=None)
        locale_manager = LocaleManager(locale_dir)
        locales = locale_manager.load_locales()
        progress.update(task, completed=True)

    if not locales:
        console.print("[yellow]No locale files found. Creating new ones if fixing...[/yellow]")

    console.print(f"[green]Loaded locales: {', '.join(locales.keys())}[/green]")

    # 3. Analyze
    analyzer = Analyzer(source_keys, locales)
    analysis = analyzer.analyze()

    # 4. Report
    has_issues = False

    for lang, missing in analysis.missing_keys.items():
        if missing:
            has_issues = True
            table = Table(title=f"Missing Keys in '{lang}'", style="red")
            table.add_column("Key", style="cyan")
            for key in sorted(missing):
                table.add_row(key)
            console.print(table)

    for lang, unused in analysis.unused_keys.items():
        if unused:
            has_issues = True
            table = Table(title=f"Unused Keys in '{lang}'", style="yellow")
            table.add_column("Key", style="magenta")
            for key in sorted(unused):
                table.add_row(key)
            console.print(table)

    if not has_issues:
        console.print("[bold green]All checks passed! No missing or unused keys found.[/bold green]")
        return

    # 5. Fix / Translate
    if args.fix or args.auto_translate:
        if args.auto_translate and not os.getenv("OPENAI_API_KEY"):
            console.print("[red]Error: OPENAI_API_KEY environment variable is required for auto-translation.[/red]")
            return

        translator = Translator() if args.auto_translate else None

        for lang, missing in analysis.missing_keys.items():
            if not missing:
                continue

            missing_list = list(missing)
            new_translations = {}

            if args.auto_translate:
                with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
                    task = progress.add_task(description=f"Translating {len(missing_list)} keys for '{lang}'...", total=None)
                    new_translations = translator.translate_keys(missing_list, target_lang=lang, source_lang=source_lang)
                    progress.update(task, completed=True)
            else:
                # Just add empty strings
                for key in missing_list:
                    new_translations[key] = ""

            # Merge
            current_locale = locales.get(lang, {})
            current_locale.update(new_translations)

            # Save
            locale_manager.save_locale(lang, current_locale)
            console.print(f"[bold green]Updated '{lang}' locale with {len(new_translations)} new keys.[/bold green]")

if __name__ == "__main__":
    main()
