import click
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from rich.panel import Panel

from doc_writer.parser import CodeParser, DocTarget
from doc_writer.generator import DocGenerator
from doc_writer.modifier import insert_docstring
from doc_writer.utils import logger, console, setup_logging

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def cli(verbose):
    """AI-Powered Documentation Generator"""
    if verbose:
        setup_logging(verbose=True)

@cli.command()
@click.option('--directory', '-d', default='.', help='Directory to scan')
def scan(directory):
    """Scan directory for missing docstrings."""
    console.print(Panel.fit("[bold cyan]Doc Writer[/bold cyan] - Scanner", border_style="cyan"))

    parser = CodeParser()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Scanning...", total=None)
        targets = parser.scan_directory(directory)
        progress.update(task, completed=1)

    if not targets:
        console.print("[green]No missing docstrings found! Great job![/green]")
        return

    table = Table(title=f"Found {len(targets)} missing docstrings")
    table.add_column("File", style="cyan")
    table.add_column("Line", style="magenta")
    table.add_column("Name", style="green")
    table.add_column("Type", style="yellow")

    for target in targets:
        table.add_row(
            os.path.relpath(target.filepath, directory),
            str(target.lineno),
            target.name,
            target.node_type
        )

    console.print(table)

@cli.command()
@click.option('--directory', '-d', default='.', help='Directory to scan and generate docs for')
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation')
def generate(directory, yes):
    """Generate and insert missing docstrings."""
    console.print(Panel.fit("[bold cyan]Doc Writer[/bold cyan] - Generator", border_style="cyan"))

    parser = CodeParser()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Scanning...", total=None)
        targets = parser.scan_directory(directory)
        progress.update(task, completed=1)

    if not targets:
        console.print("[green]No missing docstrings found![/green]")
        return

    console.print(f"[yellow]Found {len(targets)} missing docstrings.[/yellow]")

    if not yes and not Confirm.ask("Do you want to generate documentation for these items?"):
        console.print("[red]Aborted.[/red]")
        return

    generator = DocGenerator()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False,
    ) as progress:
        task = progress.add_task(description="Generating docstrings...", total=len(targets))

        success_count = 0
        for target in targets:
            progress.update(task, description=f"Processing {target.name} in {os.path.basename(target.filepath)}")

            try:
                docstring = generator.generate_docstring(target.code_snippet)
                if docstring:
                    if insert_docstring(target.filepath, target.lineno, docstring):
                        success_count += 1
            except Exception as e:
                logger.error(f"Failed to process {target.name}: {e}")

            progress.advance(task)

    console.print(f"[bold green]Successfully generated {success_count}/{len(targets)} docstrings![/bold green]")

if __name__ == '__main__':
    cli()
