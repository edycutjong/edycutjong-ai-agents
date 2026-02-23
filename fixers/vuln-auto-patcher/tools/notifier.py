from rich.console import Console
from rich.panel import Panel

console = Console()

def notify_team(message: str, level: str = "info"):
    """Simulates notifying the security team."""
    style = "bold green" if level == "success" else "bold red" if level == "error" else "bold blue"
    title = "Security Team Notification"

    console.print(Panel(message, title=title, style=style, border_style=style))
