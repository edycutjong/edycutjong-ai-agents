import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
import yaml
import json
from pathlib import Path
from typing import Optional
import sys
from dotenv import load_dotenv

from tools.diff_engine import detect_breaking_changes, APIChange, ChangeType
from tools.git_utils import get_repo, get_file_content_from_branch
from tools.ai_analysis import AIAnalyzer
from tools.notification_tool import notify_consumers
from tools.pr_blocker import fail_build

# Load environment variables from .env file
load_dotenv()

app = typer.Typer(help="API Breaking Change Detector Agent")
console = Console()

def load_spec(content: str) -> dict:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError:
            console.print("[red]Error: Unable to parse spec content (must be JSON or YAML)[/red]")
            raise typer.Exit(code=1)

@app.command()
def check(
    spec_path: str = typer.Argument(..., help="Path to the current OpenAPI spec file"),
    base_branch: str = typer.Option("main", help="The base branch to compare against"),
    block_on_breaking: bool = typer.Option(True, help="Whether to exit with error on breaking changes"),
    notify: bool = typer.Option(False, help="Whether to notify consumers about changes"),
    api_key: Optional[str] = typer.Option(None, envvar="OPENAI_API_KEY", help="OpenAI API Key")
):
    """
    Detects breaking changes in your OpenAPI spec compared to the base branch.
    """

    console.print(Panel.fit("API Breaking Change Detector", style="bold magenta"))

    # 1. Load current spec
    if not Path(spec_path).exists():
        console.print(f"[red]Error: File {spec_path} not found.[/red]")
        raise typer.Exit(code=1)

    with open(spec_path, 'r') as f:
        current_content = f.read()

    current_spec = load_spec(current_content)

    # 2. Load base spec from git
    base_spec = None
    try:
        repo = get_repo(".")
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description=f"Fetching {spec_path} from {base_branch}...", total=None)
            base_content = get_file_content_from_branch(repo, base_branch, spec_path)

        if not base_content:
            console.print(f"[red]Error: Could not retrieve {spec_path} from {base_branch}.[/red]")
            raise typer.Exit(code=1)

        base_spec = load_spec(base_content)

    except ValueError:
         console.print("[yellow]Warning: Not a git repository. Skipping base comparison.[/yellow]")
         # If not a git repo, we can't compare.
         raise typer.Exit(code=1)

    # 3. Compare
    console.print("[bold blue]Comparing specifications...[/bold blue]")
    changes = detect_breaking_changes(base_spec, current_spec)

    if not changes:
        console.print("[green]No changes detected.[/green]")
        raise typer.Exit(code=0)

    # 4. Display Diffs
    table = Table(title="Detected API Changes")
    table.add_column("Type", style="bold")
    table.add_column("Description")
    table.add_column("Location", style="dim")

    has_breaking = False
    for change in changes:
        color = "red" if change.change_type == ChangeType.BREAKING else "yellow"
        if change.change_type == ChangeType.BREAKING:
            has_breaking = True
        table.add_row(f"[{color}]{change.change_type.value}[/{color}]", change.description, change.location)

    console.print(table)

    # 5. AI Analysis
    console.print("\n[bold purple]Running AI Analysis...[/bold purple]")
    analyzer = AIAnalyzer(api_key=api_key)

    analysis = None
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Generating impact analysis...", total=None)
        analysis = analyzer.analyze(changes)

    # Display Analysis
    analysis_panel = Panel(
        Markdown(
            f"**Summary:** {analysis.summary}\n\n"
            f"**Impact Level:** {analysis.impact_level}\n\n"
            f"**Breaking:** {'Yes' if analysis.breaking else 'No'}\n\n"
            f"**Suggested Version Bump:** {analysis.version_bump}\n\n"
            f"**Changelog Entry:**\n{analysis.changelog_entry}"
        ),
        title="AI Impact Analysis",
        border_style="green" if not analysis.breaking else "red"
    )
    console.print(analysis_panel)

    # 6. Actions
    if notify:
        notify_consumers(analysis.summary)

    if block_on_breaking and has_breaking:
        fail_build("Breaking changes detected and blocking is enabled.")

if __name__ == "__main__":
    app()
