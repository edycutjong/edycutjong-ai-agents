import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.layout import Layout
from rich.live import Live
from rich.spinner import Spinner
from rich import box

# Ensure current directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from email_processor import EmailDrafter
except ImportError:
    # Fallback if running from root without package structure
    from apps.agents.email_drafter.email_processor import EmailDrafter

console = Console()

def display_welcome():
    console.print(Panel(
        "[bold cyan]Email Drafter Agent[/bold cyan]\n"
        "[dim]Powered by LangChain & OpenAI[/dim]",
        title="Welcome",
        subtitle="v1.0.0",
        border_style="cyan",
        box=box.ROUNDED
    ))

def get_email_content():
    console.print("\n[bold yellow]Please paste the email thread below.[/bold yellow]")
    console.print("[dim]Type 'END' on a new line and press Enter to finish input.[/dim]")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)

def main():
    display_welcome()

    try:
        drafter = EmailDrafter()
    except Exception as e:
        console.print(f"[bold red]Error initializing agent:[/bold red] {e}")
        console.print("[yellow]Make sure OPENAI_API_KEY is set in your environment or .env file.[/yellow]")
        return

    while True:
        email_content = get_email_content()
        if not email_content.strip():
            console.print("[red]No content provided.[/red]")
            if Prompt.ask("Try again?", choices=["y", "n"], default="y") == "n":
                break
            continue

        console.print("\n[bold green]Processing email...[/bold green]")

        with console.status("[bold blue]Thinking and drafting response...[/bold blue]", spinner="dots"):
            try:
                response = drafter.draft_email(email_content)
            except Exception as e:
                console.print(f"[bold red]Error during processing:[/bold red] {e}")
                continue

        console.print(Panel(
            Markdown(response),
            title="Draft Response",
            border_style="green",
            box=box.DOUBLE
        ))

        if not Prompt.ask("\n[bold yellow]Draft another email?[/bold yellow]", choices=["y", "n"], default="y") == "y":
            break

    console.print("\n[bold cyan]Goodbye![/bold cyan]")

if __name__ == "__main__":
    main()
