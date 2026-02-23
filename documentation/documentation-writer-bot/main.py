import os
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich.markdown import Markdown
from typing import Optional
from agent.scanner import FileScanner
from agent.generator import DocGenerator
from agent.git_handler import GitHandler
from config import config

app = typer.Typer(help="Documentation Writer Bot")
console = Console()

@app.command()
def run(
    target_dir: str = typer.Option(".", help="Target directory to scan"),
    output_dir: str = typer.Option("docs", help="Directory to save documentation"),
    tone: str = typer.Option("Professional", help="Tone of the documentation"),
    commit: bool = typer.Option(False, help="Commit changes to git"),
    dry_run: bool = typer.Option(False, help="Run without saving changes"),
    verbose: bool = typer.Option(False, help="Show detailed output"),
):
    """
    Scans the target directory and generates documentation for source files.
    """
    console.print(Panel(f"[bold blue]Documentation Writer Bot[/bold blue]\n[cyan]Target:[/cyan] {target_dir}\n[cyan]Output:[/cyan] {output_dir}\n[cyan]Tone:[/cyan] {tone}", title="[bold magenta]Welcome[/bold magenta]", border_style="green"))

    # Initialize components
    scanner = FileScanner(target_dir)
    generator = DocGenerator(tone=tone)
    git_handler = GitHandler(target_dir)

    if commit and not git_handler.is_git_repo():
        console.print("[red]Error: Target directory is not a git repository. Cannot commit changes.[/red]")
        raise typer.Exit(code=1)

    # Scan files
    with console.status("[bold green]Scanning files...[/bold green]"):
        source_files = scanner.get_source_files(extensions=[".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".c", ".cpp"])

    console.print(f"[green]Found {len(source_files)} source files.[/green]")

    if not source_files:
        console.print("[yellow]No source files found to document.[/yellow]")
        raise typer.Exit()

    # Generate documentation
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Generating documentation...", total=len(source_files))

        for file_path in source_files:
            rel_path = os.path.relpath(file_path, target_dir)
            progress.update(task, description=f"[cyan]Processing {rel_path}...")

            # Generate Doc
            doc_content = generator.generate_doc(file_path)
            mermaid_content = generator.generate_mermaid(file_path)
            api_ref_content = generator.generate_api_ref(file_path)

            full_content = f"# Documentation for `{rel_path}`\n\n"
            full_content += doc_content + "\n\n"

            if mermaid_content:
                full_content += "## Diagrams\n\n" + mermaid_content + "\n\n"

            if api_ref_content:
                full_content += "## API Reference\n\n" + api_ref_content + "\n\n"

            # Determine output path
            # output_dir/rel_path.md (replacing extension with .md)
            base_name = os.path.splitext(rel_path)[0]
            output_file = os.path.join(output_dir, base_name + ".md")

            if not dry_run:
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(full_content)

            if verbose:
                console.print(Panel(Markdown(full_content[:500] + "..."), title=f"Preview: {rel_path}", border_style="blue"))

            progress.advance(task)

    console.print(Panel(f"[bold green]Documentation generation complete![/bold green]\nProcessed {len(source_files)} files.", border_style="green"))

    if commit:
        if git_handler.has_changes():
            if not dry_run:
                console.print("[bold yellow]Committing changes...[/bold yellow]")
                success = git_handler.commit_changes(f"docs: update documentation for {len(source_files)} files")
                if success:
                    console.print("[bold green]Changes committed successfully.[/bold green]")
                else:
                    console.print("[bold red]Failed to commit changes.[/bold red]")
            else:
                console.print("[yellow]Dry run: Skipping commit.[/yellow]")
        else:
            console.print("[yellow]No changes to commit.[/yellow]")

if __name__ == "__main__":
    app()
