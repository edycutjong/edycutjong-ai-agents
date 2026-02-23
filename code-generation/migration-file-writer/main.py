import argparse
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax

# Ensure we can import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.migration_agent import MigrationAgent
from agent.schema_parser import parse_schema_text
from config import Config

console = Console()

def read_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Could not read file {filepath}: {e}")
        sys.exit(1)

def main():
    console.print(Panel.fit("[bold blue]Migration File Writer Agent[/bold blue]", subtitle="By Google Jules"))

    parser = argparse.ArgumentParser(description="Generate database migration files using AI.")
    parser.add_argument("old_schema", help="Path to the old schema file")
    parser.add_argument("new_schema", help="Path to the new schema file")
    parser.add_argument("--orm", choices=["prisma", "alembic", "knex"], default="prisma", help="Target ORM (default: prisma)")
    parser.add_argument("--api-key", help="OpenAI API Key (optional, overrides env var)")

    args = parser.parse_args()

    # Load schemas
    old_schema_content = read_file(args.old_schema)
    new_schema_content = read_file(args.new_schema)

    # Initialize Agent
    api_key = args.api_key or Config.OPENAI_API_KEY
    if not api_key:
        console.print("[bold yellow]Warning:[/bold yellow] No API Key provided. Set OPENAI_API_KEY in .env or pass --api-key.")
        # We proceed, but the agent will return an error message if called.

    agent = MigrationAgent(api_key=api_key)

    with console.status(f"[bold green]Generating {args.orm} migration...[/bold green]"):
        migration_code = agent.generate_migration(old_schema_content, new_schema_content, args.orm)

    console.print(Panel(Syntax(migration_code, "sql" if args.orm == "prisma" else "python" if args.orm == "alembic" else "javascript", theme="monokai", line_numbers=True), title="Migration Code", expand=False))

    with console.status("[bold green]Generating rollback script...[/bold green]"):
        rollback_code = agent.generate_rollback(migration_code, args.orm)

    console.print(Panel(Syntax(rollback_code, "sql" if args.orm == "prisma" else "python" if args.orm == "alembic" else "javascript", theme="monokai", line_numbers=True), title="Rollback Code", expand=False))

    with console.status("[bold green]Analyzing safety...[/bold green]"):
        safety_analysis = agent.analyze_safety(migration_code, old_schema_content, new_schema_content)

    console.print(Panel(Markdown(safety_analysis), title="Safety Analysis", expand=False))

if __name__ == "__main__":
    main()
