import sys  # pragma: no cover
import os  # pragma: no cover
import time  # pragma: no cover
from rich.console import Console  # pragma: no cover
from rich.layout import Layout  # pragma: no cover
from rich.panel import Panel  # pragma: no cover
from rich.table import Table  # pragma: no cover
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn  # pragma: no cover
from rich.text import Text  # pragma: no cover
from rich.prompt import Prompt, Confirm  # pragma: no cover
from rich import box  # pragma: no cover

# Import tools
# Assuming the script is run from the root of the app directory
try:  # pragma: no cover
    from tools.log_analyzer import LogAnalyzer  # pragma: no cover
    from tools.ast_parser import CodeScanner  # pragma: no cover
    from tools.cost_calculator import CostCalculator  # pragma: no cover
    from tools.suggester import Suggester  # pragma: no cover
    from tools.jira_integration import create_jira_ticket  # pragma: no cover
except ImportError:  # pragma: no cover
    # If run from repo root, adjust path
    sys.path.append(os.path.join(os.getcwd(), 'apps/agents/fixers/log-noise-reducer'))  # pragma: no cover
    from tools.log_analyzer import LogAnalyzer  # pragma: no cover
    from tools.ast_parser import CodeScanner  # pragma: no cover
    from tools.cost_calculator import CostCalculator  # pragma: no cover
    from tools.suggester import Suggester  # pragma: no cover
    from tools.jira_integration import create_jira_ticket  # pragma: no cover

console = Console()  # pragma: no cover

def header():  # pragma: no cover
    console.clear()  # pragma: no cover
    grid = Table.grid(expand=True)  # pragma: no cover
    grid.add_column(justify="center", ratio=1)  # pragma: no cover
    grid.add_row(  # pragma: no cover
        Panel(
            Text("LOG NOISE REDUCER", justify="center", style="bold magenta"),
            style="cyan",
            subtitle="AI-Powered Log Cleaner",
            subtitle_align="right",
            border_style="bright_magenta"
        )
    )
    console.print(grid)  # pragma: no cover

def show_progress(task_description):  # pragma: no cover
    with Progress(  # pragma: no cover
        SpinnerColumn(style="bold cyan"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None, style="magenta", complete_style="cyan"),
        transient=True,
    ) as progress:
        task = progress.add_task(description=task_description, total=100)  # pragma: no cover
        for _ in range(10):  # pragma: no cover
            time.sleep(0.05)  # pragma: no cover
            progress.update(task, advance=10)  # pragma: no cover

def main():  # pragma: no cover
    header()  # pragma: no cover

    # 1. Select Log File
    console.print("[bold cyan]Select Log Source:[/bold cyan]")  # pragma: no cover

    # Check if sample.log exists in current dir
    sample_log_path = "sample.log"  # pragma: no cover
    if not os.path.exists(sample_log_path):  # pragma: no cover
        # try relative path if run from repo root
        sample_log_path = "apps/agents/fixers/log-noise-reducer/sample.log"  # pragma: no cover

    options = ["Sample Logs", "Custom File"]  # pragma: no cover
    choice = Prompt.ask("Choose option", choices=["1", "2"], default="1")  # pragma: no cover

    log_file = sample_log_path  # pragma: no cover
    if choice == "2":  # pragma: no cover
        log_file = Prompt.ask("Enter path to log file")  # pragma: no cover
        if not os.path.exists(log_file):  # pragma: no cover
            console.print(f"[bold red]File {log_file} not found![/bold red]")  # pragma: no cover
            return  # pragma: no cover

    # 2. Select Code Directory
    code_dir = os.path.dirname(os.path.abspath(__file__)) # Default to current dir  # pragma: no cover
    if choice == "2":  # pragma: no cover
        code_dir = Prompt.ask("Enter path to source code directory", default=".")  # pragma: no cover

    # 3. Analysis
    show_progress("Reading and analyzing log patterns...")  # pragma: no cover
    analyzer = LogAnalyzer(log_file)  # pragma: no cover
    analyzer.read_logs()  # pragma: no cover
    patterns = analyzer.analyze()  # pragma: no cover
    total_logs = sum(count for _, count in patterns)  # pragma: no cover

    show_progress(f"Scanning source code in {code_dir}...")  # pragma: no cover
    scanner = CodeScanner(code_dir)  # pragma: no cover
    findings = scanner.scan()  # pragma: no cover

    # 4. Suggestions
    show_progress("Correlating data & generating insights...")  # pragma: no cover
    suggester = Suggester(patterns[:10], findings, total_logs) # Top 10 patterns  # pragma: no cover
    suggestions = suggester.generate_suggestions()  # pragma: no cover

    # 5. Display Results
    console.print("\n[bold green]Analysis Complete![/bold green]\n")  # pragma: no cover

    # Summary Panel
    cost_calc = CostCalculator()  # pragma: no cover
    estimated_cost = cost_calc.calculate_annual_projection(total_logs, avg_line_size_bytes=150)  # pragma: no cover

    summary_grid = Table.grid(expand=True, padding=(0, 2))  # pragma: no cover
    summary_grid.add_column(justify="center", ratio=1)  # pragma: no cover
    summary_grid.add_column(justify="center", ratio=1)  # pragma: no cover
    summary_grid.add_column(justify="center", ratio=1)  # pragma: no cover

    summary_grid.add_row(  # pragma: no cover
        Panel(f"[bold]{total_logs}[/bold]", title="Total Logs", border_style="cyan"),
        Panel(f"[bold]{len(patterns)}[/bold]", title="Unique Patterns", border_style="magenta"),
        Panel(f"[bold yellow]${estimated_cost:,.2f}[/bold yellow]", title="Est. Annual Cost", border_style="green"),
    )
    console.print(summary_grid)  # pragma: no cover
    console.print()  # pragma: no cover

    # Table
    table = Table(  # pragma: no cover
        title="Top High-Volume Logs & Fix Suggestions",
        box=box.ROUNDED,
        show_lines=True,
        header_style="bold cyan",
        border_style="dim"
    )
    table.add_column("Rank", style="dim", width=4, justify="center")  # pragma: no cover
    table.add_column("Pattern", style="white", ratio=3)  # pragma: no cover
    table.add_column("Count", justify="right", style="magenta")  # pragma: no cover
    table.add_column("%", justify="right", style="cyan")  # pragma: no cover
    table.add_column("Source", style="green")  # pragma: no cover
    table.add_column("Suggestion", style="bold red")  # pragma: no cover

    for i, s in enumerate(suggestions):  # pragma: no cover
        source = "Unknown"  # pragma: no cover
        if s['source']:  # pragma: no cover
            source = f"{os.path.basename(s['source']['file'])}:{s['source']['line']}"  # pragma: no cover

        pattern_display = s['pattern'][:60] + "..." if len(s['pattern']) > 60 else s['pattern']  # pragma: no cover

        suggestion_style = "bold red"  # pragma: no cover
        if s['severity'] == "Medium":  # pragma: no cover
            suggestion_style = "yellow"  # pragma: no cover
        elif s['severity'] == "Low":  # pragma: no cover
            suggestion_style = "dim green"  # pragma: no cover

        table.add_row(  # pragma: no cover
            str(i + 1),
            pattern_display,
            str(s['count']),
            f"{s['percentage']}%",
            source,
            f"[{suggestion_style}]{s['action']}[/{suggestion_style}]"
        )

    console.print(table)  # pragma: no cover

    # 6. Action
    if suggestions and Confirm.ask("\n[bold cyan]Create Jira tickets for High/Critical items?[/bold cyan]"):  # pragma: no cover
        with console.status("[bold green]Creating tickets...[/bold green]"):  # pragma: no cover
            count = 0  # pragma: no cover
            for s in suggestions:  # pragma: no cover
                if s['severity'] in ["High", "Critical"]:  # pragma: no cover
                    ticket_id = create_jira_ticket(f"Reduce Log Noise: {s['pattern'][:30]}...", s['action'])  # pragma: no cover
                    console.print(f"  ✓ Created ticket [bold]{ticket_id}[/bold] for pattern #{suggestions.index(s)+1}")  # pragma: no cover
                    count += 1  # pragma: no cover
            if count == 0:  # pragma: no cover
                console.print("  (No High/Critical items found)")  # pragma: no cover
            else:
                console.print(f"\n[bold green]Successfully created {count} tickets![/bold green]")  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    try:  # pragma: no cover
        main()  # pragma: no cover
    except KeyboardInterrupt:  # pragma: no cover
        console.print("\n[bold red]Aborted.[/bold red]")  # pragma: no cover
