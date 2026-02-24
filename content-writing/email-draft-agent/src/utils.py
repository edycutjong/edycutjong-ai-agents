"""Shared Rich console utilities."""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import logging

console = Console()


def setup_logger(name="email-draft", level=logging.INFO):
    logging.basicConfig(level=level, format="%(message)s")
    return logging.getLogger(name)


logger = setup_logger()


def print_header(title: str):
    text = Text(title, justify="center", style="bold white")
    panel = Panel(text, style="bold cyan", border_style="bold magenta", padding=(1, 2))
    console.print(panel)


def print_step(message: str):
    console.print(f"[bold cyan]➜[/bold cyan] {message}")


def print_success(message: str):
    console.print(f"[bold green]✔[/bold green] {message}")


def print_error(message: str):
    console.print(f"[bold red]✘[/bold red] {message}")
