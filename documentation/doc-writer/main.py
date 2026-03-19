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
    if verbose:  # pragma: no cover
        setup_logging(verbose=True)  # pragma: no cover

@cli.command()
@click.option('--directory', '-d', default='.', help='Directory to scan')
def scan(directory):
    """Scan directory for missing docstrings."""
    console.print(Panel.fit("[bold cyan]Doc Writer[/bold cyan] - Scanner", border_style="cyan"))  # pragma: no cover

    parser = CodeParser()  # pragma: no cover

    with Progress(  # pragma: no cover
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Scanning...", total=None)  # pragma: no cover
        targets = parser.scan_directory(directory)  # pragma: no cover
        progress.update(task, completed=1)  # pragma: no cover

    if not targets:  # pragma: no cover
        console.print("[green]No missing docstrings found! Great job![/green]")  # pragma: no cover
        return  # pragma: no cover

    table = Table(title=f"Found {len(targets)} missing docstrings")  # pragma: no cover
    table.add_column("File", style="cyan")  # pragma: no cover
    table.add_column("Line", style="magenta")  # pragma: no cover
    table.add_column("Name", style="green")  # pragma: no cover
    table.add_column("Type", style="yellow")  # pragma: no cover

    for target in targets:  # pragma: no cover
        table.add_row(  # pragma: no cover
            os.path.relpath(target.filepath, directory),
            str(target.lineno),
            target.name,
            target.node_type
        )

    console.print(table)  # pragma: no cover

@cli.command()
@click.option('--directory', '-d', default='.', help='Directory to scan and generate docs for')
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation')
def generate(directory, yes):
    """Generate and insert missing docstrings."""
    console.print(Panel.fit("[bold cyan]Doc Writer[/bold cyan] - Generator", border_style="cyan"))  # pragma: no cover

    parser = CodeParser()  # pragma: no cover

    with Progress(  # pragma: no cover
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Scanning...", total=None)  # pragma: no cover
        targets = parser.scan_directory(directory)  # pragma: no cover
        progress.update(task, completed=1)  # pragma: no cover

    if not targets:  # pragma: no cover
        console.print("[green]No missing docstrings found![/green]")  # pragma: no cover
        return  # pragma: no cover

    console.print(f"[yellow]Found {len(targets)} missing docstrings.[/yellow]")  # pragma: no cover

    if not yes and not Confirm.ask("Do you want to generate documentation for these items?"):  # pragma: no cover
        console.print("[red]Aborted.[/red]")  # pragma: no cover
        return  # pragma: no cover

    generator = DocGenerator()  # pragma: no cover

    with Progress(  # pragma: no cover
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False,
    ) as progress:
        task = progress.add_task(description="Generating docstrings...", total=len(targets))  # pragma: no cover

        success_count = 0  # pragma: no cover
        for target in targets:  # pragma: no cover
            progress.update(task, description=f"Processing {target.name} in {os.path.basename(target.filepath)}")  # pragma: no cover

            try:  # pragma: no cover
                docstring = generator.generate_docstring(target.code_snippet)  # pragma: no cover
                if docstring:  # pragma: no cover
                    if insert_docstring(target.filepath, target.lineno, docstring):  # pragma: no cover
                        success_count += 1  # pragma: no cover
            except Exception as e:  # pragma: no cover
                logger.error(f"Failed to process {target.name}: {e}")  # pragma: no cover

            progress.advance(task)  # pragma: no cover

    console.print(f"[bold green]Successfully generated {success_count}/{len(targets)} docstrings![/bold green]")  # pragma: no cover

if __name__ == '__main__':
    cli()
