import os
import sys
import asyncio
import typer
from rich.console import Console
from rich.panel import Panel

# Add current directory to sys.path so tools can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.style import Style
from dotenv import load_dotenv

# Import tools
from tools.analyzer import DependencyAnalyzer
from tools.visualizer import Visualizer
from tools.suggester import SuggestionEngine

load_dotenv()

app = typer.Typer()
console = Console()

async def analyze_project(path: str):
    """
    Main analysis workflow.
    """
    analyzer = DependencyAnalyzer(path)
    visualizer = Visualizer(os.path.join(path, "dependency-report"))
    suggester = SuggestionEngine()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:

        # Step 1: Parse Dependencies
        task1 = progress.add_task(description="Parsing package.json...", total=None)
        try:
            package_data = analyzer.parse_package_json()
            # Flatten deps
            deps = list(package_data.keys())
        except Exception as e:
            console.print(f"[bold red]Error parsing package.json:[/bold red] {e}")
            return
        progress.update(task1, completed=100)

        # Step 2: Analyze Bundle Size (Async)
        task2 = progress.add_task(description=f"Fetching bundle sizes for {len(deps)} packages...", total=len(deps))
        dependency_sizes = []

        # Limit concurrency to avoid rate limits
        sem = asyncio.Semaphore(5)

        async def fetch_size(dep):
            async with sem:
                # Get version from package.json if possible, but for now just use 'latest' or the version string
                version = package_data.get(dep, "latest").replace("^", "").replace("~", "")
                data = await analyzer.analyze_bundle_size(dep, version)
                if "error" not in data:
                    data["name"] = dep # Ensure name is present
                    dependency_sizes.append(data)
                else:
                    dependency_sizes.append({"name": dep, "size": 0, "gzip": 0, "error": data["error"]})
                progress.advance(task2)

        await asyncio.gather(*[fetch_size(dep) for dep in deps])

        # Step 3: Find Unused Dependencies
        task3 = progress.add_task(description="Scanning for unused dependencies...", total=None)
        unused_deps = analyzer.find_unused_dependencies()
        progress.update(task3, completed=100)

        # Step 4: Check Duplicates
        task4 = progress.add_task(description="Checking for duplicates...", total=None)
        duplicates = analyzer.check_duplicates()
        progress.update(task4, completed=100)

        # Step 5: AI Suggestions
        task5 = progress.add_task(description="Generating AI suggestions...", total=None)
        suggestions = suggester.get_suggestions(dependency_sizes, unused_deps)
        progress.update(task5, completed=100)

        # Step 6: Generate Report
        task6 = progress.add_task(description="Generating HTML report...", total=None)
        report_path = visualizer.generate_report(dependency_sizes, unused_deps, duplicates, suggestions)
        progress.update(task6, completed=100)

    # --- Output Results ---
    console.print(Panel.fit("[bold cyan]Dependency Bloat Analysis Complete[/bold cyan]", border_style="cyan"))

    # Summary
    total_size = sum(d.get("size", 0) for d in dependency_sizes)
    summary_table = Table(title="Summary", show_header=False, box=None)
    summary_table.add_row("Total Bundle Size", f"{total_size / 1024 / 1024:.2f} MB")
    summary_table.add_row("Unused Dependencies", f"[red]{len(unused_deps)}[/red]")
    summary_table.add_row("Duplicate Packages", f"[yellow]{len(duplicates)}[/yellow]")
    console.print(summary_table)

    # Top Heavy Dependencies
    console.print("\n[bold]Top 5 Heaviest Dependencies:[/bold]")
    sorted_deps = sorted(dependency_sizes, key=lambda x: x.get("size", 0), reverse=True)[:5]
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Package")
    table.add_column("Size (Minified)", justify="right")
    table.add_column("Size (Gzipped)", justify="right")

    for dep in sorted_deps:
        table.add_row(
            dep["name"],
            f"{dep.get('size', 0)/1024:.1f} KB",
            f"{dep.get('gzip', 0)/1024:.1f} KB"
        )
    console.print(table)

    # AI Suggestions
    if suggestions:
        console.print("\n[bold purple]AI Suggestions:[/bold purple]")
        for s in suggestions:
            console.print(f"• {s}")

    console.print(f"\n[bold green]Full report generated at:[/bold green] {report_path}")

@app.command()
def main(path: str = typer.Argument(".", help="Path to the project directory")):
    """
    Analyze dependency bloat in a JavaScript/TypeScript project.
    """
    if not os.path.exists(path):
        console.print(f"[bold red]Path not found:[/bold red] {path}")
        raise typer.Exit(code=1)

    asyncio.run(analyze_project(path))

if __name__ == "__main__":
    app()
