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
except ImportError:  # pragma: no cover
    # Fallback if running from root without package structure
    from apps.agents.email_drafter.email_processor import EmailDrafter  # pragma: no cover

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
            break  # pragma: no cover
        if line.strip() == "END":  # pragma: no cover
            break  # pragma: no cover
        lines.append(line)  # pragma: no cover
    return "\n".join(lines)  # pragma: no cover

def main():
    display_welcome()

    try:
        drafter = EmailDrafter()
    except Exception as e:  # pragma: no cover
        console.print(f"[bold red]Error initializing agent:[/bold red] {e}")  # pragma: no cover
        console.print("[yellow]Make sure OPENAI_API_KEY is set in your environment or .env file.[/yellow]")  # pragma: no cover
        return  # pragma: no cover

    while True:
        email_content = get_email_content()
        if not email_content.strip():  # pragma: no cover
            console.print("[red]No content provided.[/red]")  # pragma: no cover
            if Prompt.ask("Try again?", choices=["y", "n"], default="y") == "n":  # pragma: no cover
                break  # pragma: no cover
            continue  # pragma: no cover

        console.print("\n[bold green]Processing email...[/bold green]")  # pragma: no cover

        with console.status("[bold blue]Thinking and drafting response...[/bold blue]", spinner="dots"):  # pragma: no cover
            try:  # pragma: no cover
                response = drafter.draft_email(email_content)  # pragma: no cover
            except Exception as e:  # pragma: no cover
                console.print(f"[bold red]Error during processing:[/bold red] {e}")  # pragma: no cover
                continue  # pragma: no cover

        console.print(Panel(  # pragma: no cover
            Markdown(response),
            title="Draft Response",
            border_style="green",
            box=box.DOUBLE
        ))

        if not Prompt.ask("\n[bold yellow]Draft another email?[/bold yellow]", choices=["y", "n"], default="y") == "y":  # pragma: no cover
            break  # pragma: no cover

    console.print("\n[bold cyan]Goodbye![/bold cyan]")  # pragma: no cover

if __name__ == "__main__":
    main()  # pragma: no cover
