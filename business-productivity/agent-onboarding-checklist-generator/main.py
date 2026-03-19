import os
import yaml
import click
from lib.checklist import generate_checklist
from lib.reporter import report_json, report_markdown, report_terminal

@click.command()
@click.option("--path", default=".", help="Path to the repository to analyze.")
@click.option("--format", "fmt", type=click.Choice(["json", "markdown", "terminal"]), default="terminal", help="Output format.")
def cli(path, fmt):
    """Generates a developer onboarding checklist for a repository."""
    repo_path = os.path.abspath(path)
    
    overrides = {}
    override_file = os.path.join(repo_path, ".onboarding.yaml")
    if os.path.exists(override_file):
        try:
            with open(override_file, "r", encoding="utf-8") as f:
                overrides = yaml.safe_load(f) or {}
        except Exception:
            pass

    checklist = generate_checklist(repo_path, overrides=overrides)
    
    if fmt == "json":
        click.echo(report_json(checklist))
    elif fmt == "markdown":
        click.echo(report_markdown(checklist))
    else:
        report_terminal(checklist)

if __name__ == "__main__":
    cli()
