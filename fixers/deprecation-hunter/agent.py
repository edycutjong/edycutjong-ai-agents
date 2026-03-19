import typer  # pragma: no cover
from rich.console import Console  # pragma: no cover
from rich.progress import Progress, SpinnerColumn, TextColumn  # pragma: no cover
from rich.table import Table  # pragma: no cover
from rich.panel import Panel  # pragma: no cover
from rich.text import Text  # pragma: no cover
from rich.layout import Layout  # pragma: no cover
from rich import print as rprint  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover

# Add current directory to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # pragma: no cover

from tools.scanner import scan_directory, get_dependencies  # pragma: no cover
from tools.analyzer import DeprecationAnalyzer, DeprecationFinding  # pragma: no cover
from tools.fixer import DeprecationFixer  # pragma: no cover
from tools.reporter import generate_report  # pragma: no cover
from tools.git_manager import GitManager  # pragma: no cover

app = typer.Typer(  # pragma: no cover
    name="deprecation-hunter",
    help="AI Agent that finds and fixes deprecated library usage."
)
console = Console()  # pragma: no cover

@app.command()  # pragma: no cover
def scan(  # pragma: no cover
    path: str = typer.Argument(".", help="Path to the project directory."),
    fix: bool = typer.Option(False, "--fix", help="Automatically apply fixes."),
    pr: bool = typer.Option(False, "--pr", help="Create a PR with fixes."),
    report: bool = typer.Option(True, "--report", help="Generate an HTML report."),
    use_llm: bool = typer.Option(True, "--llm/--no-llm", help="Use LLM for analysis.")
):
    """
    Scans the codebase for deprecated usage.
    """
    console.print(Panel.fit(  # pragma: no cover
        Text("Deprecation Hunter", style="bold white on blue"),
        subtitle="AI-Powered Deprecation Finder",
        style="blue"
    ))

    # 1. Scan Dependencies
    with console.status("[bold green]Scanning dependencies...[/bold green]", spinner="dots"):  # pragma: no cover
        dependencies = get_dependencies(path)  # pragma: no cover
        console.print(f"[green]Found {len(dependencies)} dependencies.[/green]")  # pragma: no cover
        for dep, ver in dependencies.items():  # pragma: no cover
            console.print(f"  - {dep}: {ver}", style="dim")  # pragma: no cover

    # 2. Scan Files
    with console.status("[bold green]Scanning files...[/bold green]", spinner="dots"):  # pragma: no cover
        files = scan_directory(path)  # pragma: no cover
        console.print(f"[green]Found {len(files)} Python files.[/green]")  # pragma: no cover

    # 3. Analyze Files
    analyzer = DeprecationAnalyzer(use_llm=use_llm)  # pragma: no cover
    all_findings = []  # pragma: no cover

    with Progress(  # pragma: no cover
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Analyzing files...", total=len(files))  # pragma: no cover
        for file in files:  # pragma: no cover
            findings = analyzer.analyze_file(file, dependencies)  # pragma: no cover
            all_findings.extend(findings)  # pragma: no cover
            progress.advance(task)  # pragma: no cover

    # Display Results
    if not all_findings:  # pragma: no cover
        console.print("[bold green]No deprecations found! Great job![/bold green]")  # pragma: no cover
        return  # pragma: no cover

    table = Table(title="Deprecation Findings")  # pragma: no cover
    table.add_column("File", style="cyan")  # pragma: no cover
    table.add_column("Line", style="magenta")  # pragma: no cover
    table.add_column("Message", style="yellow")  # pragma: no cover
    table.add_column("Suggestion", style="green")  # pragma: no cover

    for f in all_findings:  # pragma: no cover
        table.add_row(  # pragma: no cover
            os.path.relpath(f.filepath, path),
            str(f.line_number),
            f.message,
            f.suggestion or ""
        )

    console.print(table)  # pragma: no cover

    # 4. Generate Report
    if report:  # pragma: no cover
        report_path = os.path.join(path, "deprecation_report.html")  # pragma: no cover
        generate_report(all_findings, report_path)  # pragma: no cover
        console.print(f"[bold blue]Report generated at: {report_path}[/bold blue]")  # pragma: no cover

    # 5. Fix
    if fix:  # pragma: no cover
        if typer.confirm("Do you want to apply fixes?"):  # pragma: no cover
            fixer = DeprecationFixer()  # pragma: no cover
            success_count = fixer.apply_fixes(all_findings)  # pragma: no cover
            console.print(f"[bold green]Applied {success_count} fixes.[/bold green]")  # pragma: no cover

            # 6. PR
            if pr:  # pragma: no cover
                git_mgr = GitManager(path)  # pragma: no cover
                if git_mgr.repo:  # pragma: no cover
                    branch_name = "fix/deprecations"  # pragma: no cover
                    if git_mgr.create_branch(branch_name):  # pragma: no cover
                        if git_mgr.commit_changes("chore: fix deprecated usage"):  # pragma: no cover
                            git_mgr.create_pr(  # pragma: no cover
                                title="Fix Deprecated Usage",
                                body="This PR fixes deprecated library usage found by Deprecation Hunter."
                            )
                else:
                    console.print("[red]Not a git repository, skipping PR creation.[/red]")  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    app()  # pragma: no cover
