from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text
import logging
import sys

# Initialize Rich Console
console = Console()

def setup_logger(name="code-reviewer", level=logging.INFO):
    """Sets up a logger with RichHandler."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True, markup=True)]
    )
    return logging.getLogger(name)

logger = setup_logger()

def print_header(title: str):
    """Prints a styled header."""
    text = Text(title, justify="center", style="bold white")
    panel = Panel(text, style="bold cyan", border_style="bold magenta", padding=(1, 2))
    console.print(panel)

def print_step(message: str):
    """Prints a step message."""
    console.print(f"[bold cyan]➜[/bold cyan] {message}")

def print_success(message: str):
    """Prints a success message."""
    console.print(f"[bold green]✔[/bold green] {message}")

def print_error(message: str):
    """Prints an error message."""
    console.print(f"[bold red]✘[/bold red] {message}")

def print_warning(message: str):
    """Prints a warning message."""
    console.print(f"[bold yellow]![/bold yellow] {message}")
