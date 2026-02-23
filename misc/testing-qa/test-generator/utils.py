import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text

console = Console()

def setup_logging(verbose=False):
    """Sets up the logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )
    return logging.getLogger("test_generator")

def print_banner():
    """Prints the application banner."""
    title = Text("Test Generator Agent", style="bold magenta")
    subtitle = Text("Automated Unit Test Creation", style="cyan")
    panel = Panel(
        Text.assemble(title, "\n", subtitle),
        border_style="green",
        expand=False
    )
    console.print(panel)

def print_success(message):
    """Prints a success message."""
    console.print(f"[bold green]✔[/bold green] {message}")

def print_error(message):
    """Prints an error message."""
    console.print(f"[bold red]✖[/bold red] {message}")

def print_info(message):
    """Prints an info message."""
    console.print(f"[bold blue]ℹ[/bold blue] {message}")
