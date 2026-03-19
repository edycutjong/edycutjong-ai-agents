import sys
import os
from pathlib import Path
from typing import Optional

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT))

import logging
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.prompt import Prompt

# Configure logging
logging.basicConfig(
    filename='agent.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from agent.core import FormulaWriterAgent
from agent.models import FormulaResponse

app = typer.Typer()
console = Console()

def display_response(response: FormulaResponse, target: str):
    """
    Display the formula response in a beautiful format.
    """
    console.print(Panel(f"[bold cyan]Formula for {target}[/bold cyan]", expand=False))

    # Formula - styled as code
    console.print(Panel(
        Syntax(response.formula, "text", theme="monokai", word_wrap=True),
        title="[bold green]Generated Formula[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))

    # Explanation - Markdown
    console.print(Panel(
        Markdown(response.explanation),
        title="[bold blue]Explanation[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    ))

    # Alternatives
    if response.alternatives:
        alt_table = Table(show_header=False, box=None, padding=(0, 2))
        for alt in response.alternatives:
            alt_table.add_row(f"• {alt}")
        console.print(Panel(
            alt_table,
            title="[bold yellow]Alternative Approaches[/bold yellow]",
            border_style="yellow",
            padding=(1, 2)
        ))

    # Examples
    if response.examples:
        ex_table = Table(show_header=False, box=None, padding=(0, 2))
        for ex in response.examples:
            ex_table.add_row(f"• {ex}")
        console.print(Panel(
            ex_table,
            title="[bold magenta]Usage Examples[/bold magenta]",
            border_style="magenta",
            padding=(1, 2)
        ))
    console.print()

def interactive_mode():
    """
    Run the agent in interactive REPL mode.
    """
    logger.info("Starting interactive mode.")
    console.clear()
    console.print(Panel.fit(
        "[bold green]Spreadsheet Formula Writer[/bold green]\n"
        "Type your query to generate a formula.\n"
        "Commands: [cyan]/target <app>[/cyan], [cyan]/model <name>[/cyan], [cyan]/help[/cyan], [cyan]/exit[/cyan]",
        title="Welcome",
        border_style="green"
    ))

    target = "Excel"
    model = "gpt-4o"

    while True:
        try:
            user_input = Prompt.ask(f"\n[bold cyan]({target} | {model}) >[/bold cyan]")
            user_input = user_input.strip()

            if not user_input:
                continue  # pragma: no cover

            if user_input.lower() in ("/exit", "/quit"):
                logger.info("User exited interactive mode.")
                console.print("[bold green]Goodbye![/bold green]")
                break

            if user_input.lower() == "/help":
                console.print(Panel(  # pragma: no cover
                    "• [cyan]/target <app>[/cyan]: Set target application (Excel, Google Sheets)\n"
                    "• [cyan]/model <name>[/cyan]: Set OpenAI model (gpt-4o, gpt-3.5-turbo)\n"
                    "• [cyan]/exit[/cyan]: Exit the application\n"
                    "• [cyan]/help[/cyan]: Show this help message\n"
                    "• Any other text will be treated as a query.",
                    title="Help",
                    border_style="blue"
                ))
                continue  # pragma: no cover

            if user_input.lower().startswith("/target"):
                parts = user_input.split(maxsplit=1)  # pragma: no cover
                if len(parts) > 1:  # pragma: no cover
                    new_target = parts[1]  # pragma: no cover
                    if new_target.lower() in ["excel", "google sheets", "sheets", "google_sheets"]:  # pragma: no cover
                         target = "Google Sheets" if "sheets" in new_target.lower() else "Excel"  # pragma: no cover
                         console.print(f"[green]Target set to {target}[/green]")  # pragma: no cover
                    else:
                        console.print(f"[red]Invalid target. Use 'Excel' or 'Google Sheets'[/red]")  # pragma: no cover
                else:
                    console.print(f"[yellow]Current target: {target}[/yellow]")  # pragma: no cover
                continue  # pragma: no cover

            if user_input.lower().startswith("/model"):
                parts = user_input.split(maxsplit=1)  # pragma: no cover
                if len(parts) > 1:  # pragma: no cover
                    model = parts[1]  # pragma: no cover
                    console.print(f"[green]Model set to {model}[/green]")  # pragma: no cover
                else:
                    console.print(f"[yellow]Current model: {model}[/yellow]")  # pragma: no cover
                continue  # pragma: no cover

            # Process Query
            try:
                with console.status(f"[bold green]Generating {target} formula..."):
                    agent = FormulaWriterAgent(model_name=model)
                    response = agent.generate_formula(user_input, target_application=target)

                display_response(response, target)
            except ValueError as e:  # pragma: no cover
                if "OPENAI_API_KEY" in str(e):  # pragma: no cover
                    console.print("[bold red]Error:[/bold red] OPENAI_API_KEY not found. Please set it in .env or environment variables.")  # pragma: no cover
                else:
                    console.print(f"[bold red]Error:[/bold red] {str(e)}")  # pragma: no cover
            except Exception as e:  # pragma: no cover
                console.print(f"[bold red]Error:[/bold red] {str(e)}")  # pragma: no cover

        except KeyboardInterrupt:  # pragma: no cover
            console.print("\n[bold green]Goodbye![/bold green]")  # pragma: no cover
            break  # pragma: no cover
        except Exception as e:  # pragma: no cover
            console.print(f"[bold red]Unexpected Error:[/bold red] {str(e)}")  # pragma: no cover

@app.command()
def main(
    query: Optional[str] = typer.Argument(None, help="The natural language query describing the desired formula."),
    target: str = typer.Option("Excel", "--target", "-t", help="Target application: 'Excel' or 'Google Sheets'."),
    model: str = typer.Option("gpt-4o", "--model", "-m", help="OpenAI model to use."),
):
    """
    Generate Excel or Google Sheets formulas from natural language queries.
    """
    logger.info(f"Starting application with query: {query}, target: {target}, model: {model}")
    if query is None:
        interactive_mode()
        return

    try:
        with console.status(f"[bold green]Generating {target} formula..."):
            agent = FormulaWriterAgent(model_name=model)
            response = agent.generate_formula(query, target_application=target)

        logger.info("Formula generated successfully via CLI.")
        display_response(response, target)

    except ValueError as e:
        if "OPENAI_API_KEY" in str(e):  # pragma: no cover
            logger.error("OPENAI_API_KEY missing.")  # pragma: no cover
            console.print("[bold red]Error:[/bold red] OPENAI_API_KEY not found. Please set it in .env or environment variables.")  # pragma: no cover
            raise typer.Exit(code=1)  # pragma: no cover
        else:
             logger.error(f"ValueError: {str(e)}")  # pragma: no cover
             console.print(f"[bold red]Error:[/bold red] {str(e)}")  # pragma: no cover
             raise typer.Exit(code=1)  # pragma: no cover

    except Exception as e:
        logger.error(f"Error in CLI: {str(e)}")
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
