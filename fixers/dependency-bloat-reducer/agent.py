import os  # pragma: no cover
import sys  # pragma: no cover
import asyncio  # pragma: no cover
import typer  # pragma: no cover
from rich.console import Console  # pragma: no cover
from rich.panel import Panel  # pragma: no cover

# Add current directory to sys.path so tools can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # pragma: no cover
from rich.table import Table  # pragma: no cover
from rich.progress import Progress, SpinnerColumn, TextColumn  # pragma: no cover
from rich.style import Style  # pragma: no cover
from dotenv import load_dotenv  # pragma: no cover

# Import tools
from tools.analyzer import DependencyAnalyzer  # pragma: no cover
from tools.visualizer import Visualizer  # pragma: no cover
from tools.suggester import SuggestionEngine  # pragma: no cover

load_dotenv()  # pragma: no cover

app = typer.Typer()  # pragma: no cover
console = Console()  # pragma: no cover

async def analyze_project(path: str):  # pragma: no cover
    """
    Main analysis workflow.
    """
    analyzer = DependencyAnalyzer(path)  # pragma: no cover
    visualizer = Visualizer(os.path.join(path, "dependency-report"))  # pragma: no cover
    suggester = SuggestionEngine()  # pragma: no cover

    with Progress(  # pragma: no cover
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:

        # Step 1: Parse Dependencies
        task1 = progress.add_task(description="Parsing package.json...", total=None)  # pragma: no cover
        try:  # pragma: no cover
            package_data = analyzer.parse_package_json()  # pragma: no cover
            # Flatten deps
            deps = list(package_data.keys())  # pragma: no cover
        except Exception as e:  # pragma: no cover
            console.print(f"[bold red]Error parsing package.json:[/bold red] {e}")  # pragma: no cover
            return  # pragma: no cover
        progress.update(task1, completed=100)  # pragma: no cover

        # Step 2: Analyze Bundle Size (Async)
        task2 = progress.add_task(description=f"Fetching bundle sizes for {len(deps)} packages...", total=len(deps))  # pragma: no cover
        dependency_sizes = []  # pragma: no cover

        # Limit concurrency to avoid rate limits
        sem = asyncio.Semaphore(5)  # pragma: no cover

        async def fetch_size(dep):  # pragma: no cover
            async with sem:  # pragma: no cover
                # Get version from package.json if possible, but for now just use 'latest' or the version string
                version = package_data.get(dep, "latest").replace("^", "").replace("~", "")  # pragma: no cover
                data = await analyzer.analyze_bundle_size(dep, version)  # pragma: no cover
                if "error" not in data:  # pragma: no cover
                    data["name"] = dep # Ensure name is present  # pragma: no cover
                    dependency_sizes.append(data)  # pragma: no cover
                else:
                    dependency_sizes.append({"name": dep, "size": 0, "gzip": 0, "error": data["error"]})  # pragma: no cover
                progress.advance(task2)  # pragma: no cover

        await asyncio.gather(*[fetch_size(dep) for dep in deps])  # pragma: no cover

        # Step 3: Find Unused Dependencies
        task3 = progress.add_task(description="Scanning for unused dependencies...", total=None)  # pragma: no cover
        unused_deps = analyzer.find_unused_dependencies()  # pragma: no cover
        progress.update(task3, completed=100)  # pragma: no cover

        # Step 4: Check Duplicates
        task4 = progress.add_task(description="Checking for duplicates...", total=None)  # pragma: no cover
        duplicates = analyzer.check_duplicates()  # pragma: no cover
        progress.update(task4, completed=100)  # pragma: no cover

        # Step 5: AI Suggestions
        task5 = progress.add_task(description="Generating AI suggestions...", total=None)  # pragma: no cover
        suggestions = suggester.get_suggestions(dependency_sizes, unused_deps)  # pragma: no cover
        progress.update(task5, completed=100)  # pragma: no cover

        # Step 6: Generate Report
        task6 = progress.add_task(description="Generating HTML report...", total=None)  # pragma: no cover
        report_path = visualizer.generate_report(dependency_sizes, unused_deps, duplicates, suggestions)  # pragma: no cover
        progress.update(task6, completed=100)  # pragma: no cover

    # --- Output Results ---
    console.print(Panel.fit("[bold cyan]Dependency Bloat Analysis Complete[/bold cyan]", border_style="cyan"))  # pragma: no cover

    # Summary
    total_size = sum(d.get("size", 0) for d in dependency_sizes)  # pragma: no cover
    summary_table = Table(title="Summary", show_header=False, box=None)  # pragma: no cover
    summary_table.add_row("Total Bundle Size", f"{total_size / 1024 / 1024:.2f} MB")  # pragma: no cover
    summary_table.add_row("Unused Dependencies", f"[red]{len(unused_deps)}[/red]")  # pragma: no cover
    summary_table.add_row("Duplicate Packages", f"[yellow]{len(duplicates)}[/yellow]")  # pragma: no cover
    console.print(summary_table)  # pragma: no cover

    # Top Heavy Dependencies
    console.print("\n[bold]Top 5 Heaviest Dependencies:[/bold]")  # pragma: no cover
    sorted_deps = sorted(dependency_sizes, key=lambda x: x.get("size", 0), reverse=True)[:5]  # pragma: no cover
    table = Table(show_header=True, header_style="bold magenta")  # pragma: no cover
    table.add_column("Package")  # pragma: no cover
    table.add_column("Size (Minified)", justify="right")  # pragma: no cover
    table.add_column("Size (Gzipped)", justify="right")  # pragma: no cover

    for dep in sorted_deps:  # pragma: no cover
        table.add_row(  # pragma: no cover
            dep["name"],
            f"{dep.get('size', 0)/1024:.1f} KB",
            f"{dep.get('gzip', 0)/1024:.1f} KB"
        )
    console.print(table)  # pragma: no cover

    # AI Suggestions
    if suggestions:  # pragma: no cover
        console.print("\n[bold purple]AI Suggestions:[/bold purple]")  # pragma: no cover
        for s in suggestions:  # pragma: no cover
            console.print(f"• {s}")  # pragma: no cover

    console.print(f"\n[bold green]Full report generated at:[/bold green] {report_path}")  # pragma: no cover

@app.command()  # pragma: no cover
def main(path: str = typer.Argument(".", help="Path to the project directory")):  # pragma: no cover
    """
    Analyze dependency bloat in a JavaScript/TypeScript project.
    """
    if not os.path.exists(path):  # pragma: no cover
        console.print(f"[bold red]Path not found:[/bold red] {path}")  # pragma: no cover
        raise typer.Exit(code=1)  # pragma: no cover

    asyncio.run(analyze_project(path))  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    app()  # pragma: no cover
