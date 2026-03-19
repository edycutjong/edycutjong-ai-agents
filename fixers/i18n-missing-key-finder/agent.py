import argparse  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover
from rich.console import Console  # pragma: no cover
from rich.table import Table  # pragma: no cover
from rich.panel import Panel  # pragma: no cover
from rich.progress import Progress, SpinnerColumn, TextColumn  # pragma: no cover
from rich import print as rprint  # pragma: no cover

# Add current directory to path so we can import tools
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # pragma: no cover

from tools.scanner import Scanner  # pragma: no cover
from tools.locales import LocaleManager  # pragma: no cover
from tools.analyzer import Analyzer  # pragma: no cover
from tools.translator import Translator  # pragma: no cover

console = Console()  # pragma: no cover

def main():  # pragma: no cover
    parser = argparse.ArgumentParser(description="Find missing i18n keys in your project.")  # pragma: no cover
    parser.add_argument("--source", "-s", required=True, help="Path to source code directory.")  # pragma: no cover
    parser.add_argument("--locale", "-l", required=True, help="Path to locale files directory.")  # pragma: no cover
    parser.add_argument("--source-lang", default="en", help="Source language code (default: en).")  # pragma: no cover
    parser.add_argument("--auto-translate", action="store_true", help="Auto-translate missing keys using OpenAI.")  # pragma: no cover
    parser.add_argument("--fix", action="store_true", help="Apply fixes (add missing keys to locale files).")  # pragma: no cover

    args = parser.parse_args()  # pragma: no cover

    source_dir = args.source  # pragma: no cover
    locale_dir = args.locale  # pragma: no cover
    source_lang = args.source_lang  # pragma: no cover

    console.print(Panel.fit("[bold blue]i18n Missing Key Finder[/bold blue]", border_style="blue"))  # pragma: no cover

    if not os.path.exists(source_dir):  # pragma: no cover
        console.print(f"[red]Error: Source directory '{source_dir}' does not exist.[/red]")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    if not os.path.exists(locale_dir):  # pragma: no cover
        console.print(f"[red]Error: Locale directory '{locale_dir}' does not exist.[/red]")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    # 1. Scan Source Code
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:  # pragma: no cover
        task = progress.add_task(description="Scanning source code...", total=None)  # pragma: no cover
        scanner = Scanner()  # pragma: no cover
        source_keys = scanner.scan_directory(source_dir)  # pragma: no cover
        progress.update(task, completed=True)  # pragma: no cover

    console.print(f"[green]Found {len(source_keys)} keys in source code.[/green]")  # pragma: no cover

    # 2. Load Locales
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:  # pragma: no cover
        task = progress.add_task(description="Loading locale files...", total=None)  # pragma: no cover
        locale_manager = LocaleManager(locale_dir)  # pragma: no cover
        locales = locale_manager.load_locales()  # pragma: no cover
        progress.update(task, completed=True)  # pragma: no cover

    if not locales:  # pragma: no cover
        console.print("[yellow]No locale files found. Creating new ones if fixing...[/yellow]")  # pragma: no cover

    console.print(f"[green]Loaded locales: {', '.join(locales.keys())}[/green]")  # pragma: no cover

    # 3. Analyze
    analyzer = Analyzer(source_keys, locales)  # pragma: no cover
    analysis = analyzer.analyze()  # pragma: no cover

    # 4. Report
    has_issues = False  # pragma: no cover

    for lang, missing in analysis.missing_keys.items():  # pragma: no cover
        if missing:  # pragma: no cover
            has_issues = True  # pragma: no cover
            table = Table(title=f"Missing Keys in '{lang}'", style="red")  # pragma: no cover
            table.add_column("Key", style="cyan")  # pragma: no cover
            for key in sorted(missing):  # pragma: no cover
                table.add_row(key)  # pragma: no cover
            console.print(table)  # pragma: no cover

    for lang, unused in analysis.unused_keys.items():  # pragma: no cover
        if unused:  # pragma: no cover
            has_issues = True  # pragma: no cover
            table = Table(title=f"Unused Keys in '{lang}'", style="yellow")  # pragma: no cover
            table.add_column("Key", style="magenta")  # pragma: no cover
            for key in sorted(unused):  # pragma: no cover
                table.add_row(key)  # pragma: no cover
            console.print(table)  # pragma: no cover

    if not has_issues:  # pragma: no cover
        console.print("[bold green]All checks passed! No missing or unused keys found.[/bold green]")  # pragma: no cover
        return  # pragma: no cover

    # 5. Fix / Translate
    if args.fix or args.auto_translate:  # pragma: no cover
        if args.auto_translate and not os.getenv("OPENAI_API_KEY"):  # pragma: no cover
            console.print("[red]Error: OPENAI_API_KEY environment variable is required for auto-translation.[/red]")  # pragma: no cover
            return  # pragma: no cover

        translator = Translator() if args.auto_translate else None  # pragma: no cover

        for lang, missing in analysis.missing_keys.items():  # pragma: no cover
            if not missing:  # pragma: no cover
                continue  # pragma: no cover

            missing_list = list(missing)  # pragma: no cover
            new_translations = {}  # pragma: no cover

            if args.auto_translate:  # pragma: no cover
                with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:  # pragma: no cover
                    task = progress.add_task(description=f"Translating {len(missing_list)} keys for '{lang}'...", total=None)  # pragma: no cover
                    new_translations = translator.translate_keys(missing_list, target_lang=lang, source_lang=source_lang)  # pragma: no cover
                    progress.update(task, completed=True)  # pragma: no cover
            else:
                # Just add empty strings
                for key in missing_list:  # pragma: no cover
                    new_translations[key] = ""  # pragma: no cover

            # Merge
            current_locale = locales.get(lang, {})  # pragma: no cover
            current_locale.update(new_translations)  # pragma: no cover

            # Save
            locale_manager.save_locale(lang, current_locale)  # pragma: no cover
            console.print(f"[bold green]Updated '{lang}' locale with {len(new_translations)} new keys.[/bold green]")  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
