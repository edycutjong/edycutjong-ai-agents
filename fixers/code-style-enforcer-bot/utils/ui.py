from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.theme import Theme
import time

custom_theme = Theme({
    "info": "cyan",
    "warning": "magenta",
    "error": "bold red",
    "success": "bold green",
    "highlight": "bold yellow",
    "code": "bold white on black",
})

console = Console(theme=custom_theme)

def print_header():
    title = Text("Code Style Enforcer Bot", style="bold white")
    subtitle = Text("Friendly bot to enforce and fix style", style="dim white")

    panel = Panel(
        Align.center(title + "\n" + subtitle),
        border_style="cyan",
        title="✨ AGENT ✨",
        title_align="left",
        padding=(1, 2),
    )
    console.print(panel)

def print_success(message):
    console.print(f"[success]✔ {message}[/success]")  # pragma: no cover

def print_error(message):
    console.print(f"[error]✖ {message}[/error]")  # pragma: no cover

def print_warning(message):
    console.print(f"[warning]! {message}[/warning]")

def print_info(message):
    console.print(f"[info]ℹ {message}[/info]")

def print_code_block(code, language="python", title="Code Snippet"):
    from rich.syntax import Syntax  # pragma: no cover
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)  # pragma: no cover
    console.print(Panel(syntax, title=title, border_style="cyan"))  # pragma: no cover

def spinner(message="Processing..."):
    return console.status(f"[bold cyan]{message}[/bold cyan]", spinner="dots")  # pragma: no cover

def ask_user(prompt):
    return console.input(f"[bold yellow]{prompt}[/bold yellow] ")  # pragma: no cover
