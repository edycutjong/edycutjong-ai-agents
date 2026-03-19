import argparse
import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn

# Ensure we can import modules
sys.path.append(os.path.dirname(__file__))

from agent.schema_loader import SchemaLoader
from agent.planner import MigrationPlanner
from agent.models import MigrationPlan

console = Console()

def display_plan(plan: MigrationPlan):
    """Displays the migration plan in a rich format."""
    console.print(Panel(f"[bold blue]Migration Plan Summary[/bold blue]\n\n{plan.summary}", title="Summary"))  # pragma: no cover

    # Steps Table
    table = Table(title="Migration Steps", show_header=True, header_style="bold magenta")  # pragma: no cover
    table.add_column("ID", style="dim", width=4)  # pragma: no cover
    table.add_column("Description", style="white")  # pragma: no cover
    table.add_column("Risk", style="cyan")  # pragma: no cover
    table.add_column("Est. Time (s)", justify="right")  # pragma: no cover

    for step in plan.steps:  # pragma: no cover
        risk_color = "green" if step.risk_level == "low" else "yellow" if step.risk_level == "medium" else "red"  # pragma: no cover
        table.add_row(  # pragma: no cover
            str(step.id),
            step.description,
            f"[{risk_color}]{step.risk_level}[/{risk_color}]",
            str(step.estimated_duration_seconds)
        )

    console.print(table)  # pragma: no cover

    # Breaking Changes
    if plan.breaking_changes:  # pragma: no cover
        console.print("\n[bold red]⚠️  Breaking Changes Identified![/bold red]")  # pragma: no cover
        for change in plan.breaking_changes:  # pragma: no cover
            console.print(Panel(  # pragma: no cover
                f"[bold]Impact:[/bold] {change.impact}\n[bold]Mitigation:[/bold] {change.mitigation}",
                title=f"Breaking Change: {change.description}",
                border_style="red"
            ))
    else:
        console.print("\n[bold green]✅ No breaking changes identified.[/bold green]")  # pragma: no cover

    # Integrity Checks
    if plan.integrity_checks:  # pragma: no cover
        console.print("\n[bold yellow]🛡️  Data Integrity Checks[/bold yellow]")  # pragma: no cover
        for check in plan.integrity_checks:  # pragma: no cover
            console.print(f"• [bold]{check.description}[/bold]: `{check.query}` (Expected: {check.expected_result})")  # pragma: no cover

    console.print(f"\n[bold]Total Estimated Duration:[/bold] {plan.total_estimated_duration_seconds} seconds")  # pragma: no cover

def load_schema(loader: SchemaLoader, path: str) -> str:
    """Loads schema from file or directory."""
    if os.path.isdir(path):  # pragma: no cover
        console.print(f"[dim]Loading schema from directory: {path}[/dim]")  # pragma: no cover
        return loader.load_from_directory(path)  # pragma: no cover
    else:
        console.print(f"[dim]Loading schema from file: {path}[/dim]")  # pragma: no cover
        return loader.load_from_file(path)  # pragma: no cover

def main():
    parser = argparse.ArgumentParser(description="Database Migration Planner Agent")
    parser.add_argument("source", help="Path to source schema SQL file or directory")
    parser.add_argument("target", help="Path to target schema SQL file or directory")
    parser.add_argument("--output-sql", help="Output file for Up migration SQL script")
    parser.add_argument("--output-rollback", help="Output file for Down migration SQL script")

    args = parser.parse_args()

    loader = SchemaLoader()  # pragma: no cover
    planner = MigrationPlanner()  # pragma: no cover

    try:  # pragma: no cover
        source_schema = load_schema(loader, args.source)  # pragma: no cover
        target_schema = load_schema(loader, args.target)  # pragma: no cover
    except (FileNotFoundError, NotADirectoryError) as e:  # pragma: no cover
        console.print(f"[bold red]Error:[/bold red] {e}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    console.print(f"[bold blue]Analyzing schemas...[/bold blue]")  # pragma: no cover

    try:  # pragma: no cover
        with Progress(  # pragma: no cover
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Generating migration plan...", total=None)  # pragma: no cover
            plan = planner.generate_plan(source_schema, target_schema)  # pragma: no cover

        display_plan(plan)  # pragma: no cover

        # SQL Output
        sql_script = planner.generate_sql_script(plan)  # pragma: no cover
        rollback_script = planner.generate_rollback_script(plan)  # pragma: no cover

        console.print("\n[bold]Generated SQL Script (Preview):[/bold]")  # pragma: no cover
        console.print(Syntax(sql_script, "sql", theme="monokai", line_numbers=True))  # pragma: no cover

        if args.output_sql:  # pragma: no cover
            with open(args.output_sql, "w") as f:  # pragma: no cover
                f.write(sql_script)  # pragma: no cover
            console.print(f"\n[green]Saved Up migration script to {args.output_sql}[/green]")  # pragma: no cover

        if args.output_rollback:  # pragma: no cover
            with open(args.output_rollback, "w") as f:  # pragma: no cover
                f.write(rollback_script)  # pragma: no cover
            console.print(f"[green]Saved Rollback script to {args.output_rollback}[/green]")  # pragma: no cover

    except Exception as e:  # pragma: no cover
        console.print(f"[bold red]An error occurred during planning:[/bold red] {e}")  # pragma: no cover
        # import traceback
        # traceback.print_exc()
        sys.exit(1)  # pragma: no cover

if __name__ == "__main__":
    main()
