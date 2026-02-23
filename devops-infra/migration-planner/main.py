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
    console.print(Panel(f"[bold blue]Migration Plan Summary[/bold blue]\n\n{plan.summary}", title="Summary"))

    # Steps Table
    table = Table(title="Migration Steps", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Description", style="white")
    table.add_column("Risk", style="cyan")
    table.add_column("Est. Time (s)", justify="right")

    for step in plan.steps:
        risk_color = "green" if step.risk_level == "low" else "yellow" if step.risk_level == "medium" else "red"
        table.add_row(
            str(step.id),
            step.description,
            f"[{risk_color}]{step.risk_level}[/{risk_color}]",
            str(step.estimated_duration_seconds)
        )

    console.print(table)

    # Breaking Changes
    if plan.breaking_changes:
        console.print("\n[bold red]⚠️  Breaking Changes Identified![/bold red]")
        for change in plan.breaking_changes:
            console.print(Panel(
                f"[bold]Impact:[/bold] {change.impact}\n[bold]Mitigation:[/bold] {change.mitigation}",
                title=f"Breaking Change: {change.description}",
                border_style="red"
            ))
    else:
        console.print("\n[bold green]✅ No breaking changes identified.[/bold green]")

    # Integrity Checks
    if plan.integrity_checks:
        console.print("\n[bold yellow]🛡️  Data Integrity Checks[/bold yellow]")
        for check in plan.integrity_checks:
            console.print(f"• [bold]{check.description}[/bold]: `{check.query}` (Expected: {check.expected_result})")

    console.print(f"\n[bold]Total Estimated Duration:[/bold] {plan.total_estimated_duration_seconds} seconds")

def load_schema(loader: SchemaLoader, path: str) -> str:
    """Loads schema from file or directory."""
    if os.path.isdir(path):
        console.print(f"[dim]Loading schema from directory: {path}[/dim]")
        return loader.load_from_directory(path)
    else:
        console.print(f"[dim]Loading schema from file: {path}[/dim]")
        return loader.load_from_file(path)

def main():
    parser = argparse.ArgumentParser(description="Database Migration Planner Agent")
    parser.add_argument("source", help="Path to source schema SQL file or directory")
    parser.add_argument("target", help="Path to target schema SQL file or directory")
    parser.add_argument("--output-sql", help="Output file for Up migration SQL script")
    parser.add_argument("--output-rollback", help="Output file for Down migration SQL script")

    args = parser.parse_args()

    loader = SchemaLoader()
    planner = MigrationPlanner()

    try:
        source_schema = load_schema(loader, args.source)
        target_schema = load_schema(loader, args.target)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

    console.print(f"[bold blue]Analyzing schemas...[/bold blue]")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Generating migration plan...", total=None)
            plan = planner.generate_plan(source_schema, target_schema)

        display_plan(plan)

        # SQL Output
        sql_script = planner.generate_sql_script(plan)
        rollback_script = planner.generate_rollback_script(plan)

        console.print("\n[bold]Generated SQL Script (Preview):[/bold]")
        console.print(Syntax(sql_script, "sql", theme="monokai", line_numbers=True))

        if args.output_sql:
            with open(args.output_sql, "w") as f:
                f.write(sql_script)
            console.print(f"\n[green]Saved Up migration script to {args.output_sql}[/green]")

        if args.output_rollback:
            with open(args.output_rollback, "w") as f:
                f.write(rollback_script)
            console.print(f"[green]Saved Rollback script to {args.output_rollback}[/green]")

    except Exception as e:
        console.print(f"[bold red]An error occurred during planning:[/bold red] {e}")
        # import traceback
        # traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
