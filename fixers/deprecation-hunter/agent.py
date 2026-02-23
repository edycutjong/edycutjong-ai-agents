import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich import print as rprint
import os
import sys

# Add current directory to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.scanner import scan_directory, get_dependencies
from tools.analyzer import DeprecationAnalyzer, DeprecationFinding
from tools.fixer import DeprecationFixer
from tools.reporter import generate_report
from tools.git_manager import GitManager

app = typer.Typer(
    name="deprecation-hunter",
    help="AI Agent that finds and fixes deprecated library usage."
)
console = Console()

@app.command()
def scan(
    path: str = typer.Argument(".", help="Path to the project directory."),
    fix: bool = typer.Option(False, "--fix", help="Automatically apply fixes."),
    pr: bool = typer.Option(False, "--pr", help="Create a PR with fixes."),
    report: bool = typer.Option(True, "--report", help="Generate an HTML report."),
    use_llm: bool = typer.Option(True, "--llm/--no-llm", help="Use LLM for analysis.")
):
    """
    Scans the codebase for deprecated usage.
    """
    console.print(Panel.fit(
        Text("Deprecation Hunter", style="bold white on blue"),
        subtitle="AI-Powered Deprecation Finder",
        style="blue"
    ))

    # 1. Scan Dependencies
    with console.status("[bold green]Scanning dependencies...[/bold green]", spinner="dots"):
        dependencies = get_dependencies(path)
        console.print(f"[green]Found {len(dependencies)} dependencies.[/green]")
        for dep, ver in dependencies.items():
            console.print(f"  - {dep}: {ver}", style="dim")

    # 2. Scan Files
    with console.status("[bold green]Scanning files...[/bold green]", spinner="dots"):
        files = scan_directory(path)
        console.print(f"[green]Found {len(files)} Python files.[/green]")

    # 3. Analyze Files
    analyzer = DeprecationAnalyzer(use_llm=use_llm)
    all_findings = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Analyzing files...", total=len(files))
        for file in files:
            findings = analyzer.analyze_file(file, dependencies)
            all_findings.extend(findings)
            progress.advance(task)

    # Display Results
    if not all_findings:
        console.print("[bold green]No deprecations found! Great job![/bold green]")
        return

    table = Table(title="Deprecation Findings")
    table.add_column("File", style="cyan")
    table.add_column("Line", style="magenta")
    table.add_column("Message", style="yellow")
    table.add_column("Suggestion", style="green")

    for f in all_findings:
        table.add_row(
            os.path.relpath(f.filepath, path),
            str(f.line_number),
            f.message,
            f.suggestion or ""
        )

    console.print(table)

    # 4. Generate Report
    if report:
        report_path = os.path.join(path, "deprecation_report.html")
        generate_report(all_findings, report_path)
        console.print(f"[bold blue]Report generated at: {report_path}[/bold blue]")

    # 5. Fix
    if fix:
        if typer.confirm("Do you want to apply fixes?"):
            fixer = DeprecationFixer()
            success_count = fixer.apply_fixes(all_findings)
            console.print(f"[bold green]Applied {success_count} fixes.[/bold green]")

            # 6. PR
            if pr:
                git_mgr = GitManager(path)
                if git_mgr.repo:
                    branch_name = "fix/deprecations"
                    if git_mgr.create_branch(branch_name):
                        if git_mgr.commit_changes("chore: fix deprecated usage"):
                            git_mgr.create_pr(
                                title="Fix Deprecated Usage",
                                body="This PR fixes deprecated library usage found by Deprecation Hunter."
                            )
                else:
                    console.print("[red]Not a git repository, skipping PR creation.[/red]")

if __name__ == "__main__":
    app()
