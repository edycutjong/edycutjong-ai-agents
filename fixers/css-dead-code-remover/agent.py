import typer
import os
import logging
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import print as rprint

# Import tools
try:
    from tools.parser import parse_css_file
    from tools.scanner import scan_directory, scan_file
    from tools.smart_scanner import analyze_component_with_llm
    from tools.detector import find_unused_rules, audit_media_queries
    from tools.cleaner import purge_css, minify_css
    from tools.reporter import generate_report
    from tools.crawler import crawl_url, compare_screenshots
except ImportError:
    # Try absolute imports if running from root
    try:
        from apps.agents.fixers.css_dead_code_remover.tools.parser import parse_css_file
        from apps.agents.fixers.css_dead_code_remover.tools.scanner import scan_directory, scan_file
        from apps.agents.fixers.css_dead_code_remover.tools.smart_scanner import analyze_component_with_llm
        from apps.agents.fixers.css_dead_code_remover.tools.detector import find_unused_rules, audit_media_queries
        from apps.agents.fixers.css_dead_code_remover.tools.cleaner import purge_css, minify_css
        from apps.agents.fixers.css_dead_code_remover.tools.reporter import generate_report
        from apps.agents.fixers.css_dead_code_remover.tools.crawler import crawl_url, compare_screenshots
    except ImportError as e:
        print(f"Error importing tools: {e}")
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from tools.parser import parse_css_file
        from tools.scanner import scan_directory, scan_file
        from tools.smart_scanner import analyze_component_with_llm
        from tools.detector import find_unused_rules, audit_media_queries
        from tools.cleaner import purge_css, minify_css
        from tools.reporter import generate_report
        from tools.crawler import crawl_url, compare_screenshots

app = typer.Typer()
console = Console()
logging.basicConfig(level=logging.ERROR) # Suppress debug logs

@app.command()
def scan(
    directory: str = typer.Argument(..., help="Directory to scan for usage"),
    css_file: str = typer.Argument(..., help="CSS file to analyze"),
    output_report: str = typer.Option("report.html", help="Path to save the HTML report"),
    safelist: List[str] = typer.Option([], help="List of selectors to keep (regex supported)"),
    smart: bool = typer.Option(False, help="Enable smart scanning with LLM (requires OPENAI_API_KEY)"),
    crawl: Optional[str] = typer.Option(None, help="URL to crawl for additional verification")
):
    """
    Scan a directory and CSS file to identify unused CSS rules.
    """
    console.print(Panel(f"Scanning [bold cyan]{directory}[/bold cyan] against [bold yellow]{css_file}[/bold yellow]", title="CSS Dead Code Remover", border_style="magenta"))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:

        # Step 1: Parse CSS
        task1 = progress.add_task("Parsing CSS file...", total=None)
        rules = parse_css_file(css_file)
        progress.update(task1, completed=True)
        console.print(f"[green]✔[/green] Parsed {len(rules)} CSS rules.")

        # Step 2: Scan Directory (with Smart Scan if enabled)
        task2 = progress.add_task("Scanning project files...", total=None)
        if smart:
             console.print("[yellow]⚠[/yellow] Smart scan enabled. This might take longer due to LLM analysis.")

        used_selectors = scan_directory(directory, smart_scan=smart)
        progress.update(task2, completed=True)
        console.print(f"[green]✔[/green] Found {len(used_selectors)} unique selectors in codebase.")

        # Step 3: Crawl (Optional)
        if crawl:
            task3 = progress.add_task(f"Crawling {crawl}...", total=None)
            screenshot = crawl_url(crawl)
            if screenshot:
                console.print(f"[green]✔[/green] Captured screenshot: {screenshot}")
            progress.update(task3, completed=True)

        # Step 4: Detect Unused
        task4 = progress.add_task("Identifying unused rules...", total=None)
        unused_rules = find_unused_rules(rules, used_selectors, safelist)
        progress.update(task4, completed=True)

        # Step 5: Audit Media Queries
        media_stats = audit_media_queries(rules)

        # Report
        unused_count = len(unused_rules)
        savings = unused_count * 0.05 # Rough estimate KB

        table = Table(title="Scan Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        table.add_row("Total Rules", str(len(rules)))
        table.add_row("Unused Rules", str(unused_count))
        table.add_row("Efficiency", f"{int(((len(rules)-unused_count)/len(rules))*100)}%")

        console.print(table)

        generate_report(output_report, len(rules), unused_rules, media_stats, savings)
        console.print(f"[bold green]Report generated at {output_report}[/bold green]")

@app.command()
def purge(
    css_file: str = typer.Argument(..., help="Source CSS file"),
    output_file: str = typer.Argument(..., help="Output path for cleaned CSS"),
    directory: str = typer.Option(..., help="Directory to scan for usage"), # Required to know what to purge
    minify: bool = typer.Option(False, help="Minify the output CSS")
):
    """
    Purge unused CSS rules from a file and optionally minify.
    """
    console.print(Panel(f"Purging [bold yellow]{css_file}[/bold yellow]", title="CSS Purge", border_style="red"))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:

        # Parse & Scan
        progress.add_task("Analyzing...", total=None)
        rules = parse_css_file(css_file)
        # Assuming purge doesn't use smart scan by default as it's dangerous without review?
        # Or should we allow it? Typer options default to False.
        # Let's keep purge safe and simple (regex only) unless we add flag to purge command.
        # For now, default False.
        used_selectors = scan_directory(directory, smart_scan=False)
        unused_rules = find_unused_rules(rules, used_selectors)

        # Purge
        progress.add_task("Purging...", total=None)
        cleaned_css = purge_css(css_file, unused_rules)

        # Minify
        if minify:
            progress.add_task("Minifying...", total=None)
            cleaned_css = minify_css(cleaned_css)

        # Write
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_css)

    console.print(f"[bold green]Cleaned CSS saved to {output_file}[/bold green]")
    original_size = os.path.getsize(css_file)
    new_size = os.path.getsize(output_file)
    reduction = ((original_size - new_size) / original_size) * 100
    console.print(f"Size reduction: [bold]{reduction:.2f}%[/bold] ({original_size}B -> {new_size}B)")

if __name__ == "__main__":
    app()
