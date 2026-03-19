import click
import yaml
import sys
from rich.console import Console
from pathlib import Path
from typing import Dict, Any

from lib.migration_parser import parse_migrations
from lib.orm_parser import parse_orm_models
from lib.differ import calculate_drift
from lib.reporter import format_markdown, format_json, format_table

console = Console()

def load_config(config_path: str) -> Dict[str, Any]:
    """Loads configuration from a YAML file."""
    path = Path(config_path)
    if not path.exists():
        return {
            "migrations": ["migrations/"],
            "orm_models": ["schema.prisma"],
            "dialect": "postgres",
            "ignore": {"tables": [], "columns": [], "drift_types": []}
        }
    with open(path, "r") as f:
        return yaml.safe_load(f)

@click.command()
@click.option("--migrations-dir", "-m", multiple=True, help="Directory containing SQL migration files.")
@click.option("--orm-file", "-o", multiple=True, help="Path to ORM definition file (e.g., schema.prisma).")
@click.option("--config", "-c", default="config.yaml", help="Path to config file.")
@click.option("--format", "-f", type=click.Choice(["table", "json", "markdown"]), default="table", help="Output format.")
@click.option("--dialect", "-d", default="postgres", help="SQL dialect for parsing migrations.")
def cli(migrations_dir, orm_file, config, format, dialect):
    """Detects drift between SQL database migrations and ORM model definitions."""
    
    cfg = load_config(config)
    
    # Override config with CLI arguments if provided
    migrations_paths = migrations_dir if migrations_dir else cfg.get("migrations", ["migrations/"])
    orm_paths = orm_file if orm_file else cfg.get("orm_models", ["schema.prisma"])
    sql_dialect = dialect if dialect != "postgres" else cfg.get("dialect", "postgres")
    ignore_rules = cfg.get("ignore", {})
    
    expected_schema = {}
    for path_str in migrations_paths:
        path = Path(path_str)
        if path.is_dir() or path.is_file():
            expected_schema = parse_migrations(path, sql_dialect, expected_schema)
    
    actual_models = {}
    for path_str in orm_paths:
        path = Path(path_str)
        if path.is_dir() or path.is_file():
            actual_models = parse_orm_models(path, actual_models)

    drifts = calculate_drift(expected_schema, actual_models, ignore_rules)

    if format == "json":
        console.print_json(format_json(drifts))
    elif format == "markdown":
        console.print(format_markdown(drifts))
    else:
        table = format_table(drifts)
        console.print(table)
    
    if drifts:
        console.print(f"[bold red]Drift detected! Found {sum(len(d) for d in drifts.values())} issue(s).[/bold red]")
        sys.exit(1)
    else:
        console.print("[bold green]No schema drift detected. Mappings are in sync.[/bold green]")
        sys.exit(0)

if __name__ == "__main__": # pragma: no cover
    cli()
