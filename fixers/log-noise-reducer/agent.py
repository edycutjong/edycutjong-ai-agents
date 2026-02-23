import sys
import os
import time
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich import box

# Import tools
# Assuming the script is run from the root of the app directory
try:
    from tools.log_analyzer import LogAnalyzer
    from tools.ast_parser import CodeScanner
    from tools.cost_calculator import CostCalculator
    from tools.suggester import Suggester
    from tools.jira_integration import create_jira_ticket
except ImportError:
    # If run from repo root, adjust path
    sys.path.append(os.path.join(os.getcwd(), 'apps/agents/fixers/log-noise-reducer'))
    from tools.log_analyzer import LogAnalyzer
    from tools.ast_parser import CodeScanner
    from tools.cost_calculator import CostCalculator
    from tools.suggester import Suggester
    from tools.jira_integration import create_jira_ticket

console = Console()

def header():
    console.clear()
    grid = Table.grid(expand=True)
    grid.add_column(justify="center", ratio=1)
    grid.add_row(
        Panel(
            Text("LOG NOISE REDUCER", justify="center", style="bold magenta"),
            style="cyan",
            subtitle="AI-Powered Log Cleaner",
            subtitle_align="right",
            border_style="bright_magenta"
        )
    )
    console.print(grid)

def show_progress(task_description):
    with Progress(
        SpinnerColumn(style="bold cyan"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None, style="magenta", complete_style="cyan"),
        transient=True,
    ) as progress:
        task = progress.add_task(description=task_description, total=100)
        for _ in range(10):
            time.sleep(0.05)
            progress.update(task, advance=10)

def main():
    header()

    # 1. Select Log File
    console.print("[bold cyan]Select Log Source:[/bold cyan]")

    # Check if sample.log exists in current dir
    sample_log_path = "sample.log"
    if not os.path.exists(sample_log_path):
        # try relative path if run from repo root
        sample_log_path = "apps/agents/fixers/log-noise-reducer/sample.log"

    options = ["Sample Logs", "Custom File"]
    choice = Prompt.ask("Choose option", choices=["1", "2"], default="1")

    log_file = sample_log_path
    if choice == "2":
        log_file = Prompt.ask("Enter path to log file")
        if not os.path.exists(log_file):
            console.print(f"[bold red]File {log_file} not found![/bold red]")
            return

    # 2. Select Code Directory
    code_dir = os.path.dirname(os.path.abspath(__file__)) # Default to current dir
    if choice == "2":
        code_dir = Prompt.ask("Enter path to source code directory", default=".")

    # 3. Analysis
    show_progress("Reading and analyzing log patterns...")
    analyzer = LogAnalyzer(log_file)
    analyzer.read_logs()
    patterns = analyzer.analyze()
    total_logs = sum(count for _, count in patterns)

    show_progress(f"Scanning source code in {code_dir}...")
    scanner = CodeScanner(code_dir)
    findings = scanner.scan()

    # 4. Suggestions
    show_progress("Correlating data & generating insights...")
    suggester = Suggester(patterns[:10], findings, total_logs) # Top 10 patterns
    suggestions = suggester.generate_suggestions()

    # 5. Display Results
    console.print("\n[bold green]Analysis Complete![/bold green]\n")

    # Summary Panel
    cost_calc = CostCalculator()
    estimated_cost = cost_calc.calculate_annual_projection(total_logs, avg_line_size_bytes=150)

    summary_grid = Table.grid(expand=True, padding=(0, 2))
    summary_grid.add_column(justify="center", ratio=1)
    summary_grid.add_column(justify="center", ratio=1)
    summary_grid.add_column(justify="center", ratio=1)

    summary_grid.add_row(
        Panel(f"[bold]{total_logs}[/bold]", title="Total Logs", border_style="cyan"),
        Panel(f"[bold]{len(patterns)}[/bold]", title="Unique Patterns", border_style="magenta"),
        Panel(f"[bold yellow]${estimated_cost:,.2f}[/bold yellow]", title="Est. Annual Cost", border_style="green"),
    )
    console.print(summary_grid)
    console.print()

    # Table
    table = Table(
        title="Top High-Volume Logs & Fix Suggestions",
        box=box.ROUNDED,
        show_lines=True,
        header_style="bold cyan",
        border_style="dim"
    )
    table.add_column("Rank", style="dim", width=4, justify="center")
    table.add_column("Pattern", style="white", ratio=3)
    table.add_column("Count", justify="right", style="magenta")
    table.add_column("%", justify="right", style="cyan")
    table.add_column("Source", style="green")
    table.add_column("Suggestion", style="bold red")

    for i, s in enumerate(suggestions):
        source = "Unknown"
        if s['source']:
            source = f"{os.path.basename(s['source']['file'])}:{s['source']['line']}"

        pattern_display = s['pattern'][:60] + "..." if len(s['pattern']) > 60 else s['pattern']

        suggestion_style = "bold red"
        if s['severity'] == "Medium":
            suggestion_style = "yellow"
        elif s['severity'] == "Low":
            suggestion_style = "dim green"

        table.add_row(
            str(i + 1),
            pattern_display,
            str(s['count']),
            f"{s['percentage']}%",
            source,
            f"[{suggestion_style}]{s['action']}[/{suggestion_style}]"
        )

    console.print(table)

    # 6. Action
    if suggestions and Confirm.ask("\n[bold cyan]Create Jira tickets for High/Critical items?[/bold cyan]"):
        with console.status("[bold green]Creating tickets...[/bold green]"):
            count = 0
            for s in suggestions:
                if s['severity'] in ["High", "Critical"]:
                    ticket_id = create_jira_ticket(f"Reduce Log Noise: {s['pattern'][:30]}...", s['action'])
                    console.print(f"  ✓ Created ticket [bold]{ticket_id}[/bold] for pattern #{suggestions.index(s)+1}")
                    count += 1
            if count == 0:
                console.print("  (No High/Critical items found)")
            else:
                console.print(f"\n[bold green]Successfully created {count} tickets![/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Aborted.[/bold red]")
