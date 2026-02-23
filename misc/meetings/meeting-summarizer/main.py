import click
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.layout import Layout
from rich import print as rprint
import pyfiglet

# Add the current directory to sys.path to allow relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import read_file
from agent_config import get_summary_chain, get_action_items_chain, get_email_chain, get_sentiment_chain

console = Console()

def print_banner():
    banner_text = pyfiglet.figlet_format("Meeting Summarizer", font="slant")
    console.print(Text(banner_text, style="bold cyan"))
    console.print(Panel.fit("Analyze meeting transcripts with AI", style="bold magenta"))

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def main(file_path):
    """
    Analyzes a meeting transcript (TXT or VTT) and provides:
    - Key Decisions Summary
    - Action Items
    - Sentiment Analysis
    - Draft Follow-up Email
    """
    print_banner()

    try:
        with console.status("[bold green]Reading transcript...", spinner="dots"):
            transcript = read_file(file_path)
            console.print(f"[bold green]✓[/] Successfully read {file_path}")

        # Initialize chains
        summary_chain = get_summary_chain()
        action_items_chain = get_action_items_chain()
        email_chain = get_email_chain()
        sentiment_chain = get_sentiment_chain()

        results = {}

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task1 = progress.add_task("[cyan]Summarizing Key Decisions...", total=None)
            results['summary'] = summary_chain.invoke({"transcript": transcript})
            progress.update(task1, completed=True)
            progress.console.print("[bold green]✓[/] Summary generated")

            task2 = progress.add_task("[magenta]Extracting Action Items...", total=None)
            results['action_items'] = action_items_chain.invoke({"transcript": transcript})
            progress.update(task2, completed=True)
            progress.console.print("[bold green]✓[/] Action Items extracted")

            task3 = progress.add_task("[yellow]Analyzing Sentiment...", total=None)
            results['sentiment'] = sentiment_chain.invoke({"transcript": transcript})
            progress.update(task3, completed=True)
            progress.console.print("[bold green]✓[/] Sentiment analyzed")

            task4 = progress.add_task("[blue]Drafting Email...", total=None)
            results['email'] = email_chain.invoke({"transcript": transcript})
            progress.update(task4, completed=True)
            progress.console.print("[bold green]✓[/] Email drafted")

        # Display Results
        console.rule("[bold cyan]Results[/]")

        console.print(Panel(Markdown(results['summary']), title="[bold cyan]Key Decisions[/]", border_style="cyan"))
        console.print(Panel(Markdown(results['action_items']), title="[bold magenta]Action Items[/]", border_style="magenta"))
        console.print(Panel(Markdown(results['sentiment']), title="[bold yellow]Sentiment Analysis[/]", border_style="yellow"))
        console.print(Panel(Markdown(results['email']), title="[bold blue]Draft Email[/]", border_style="blue"))

        console.print(Panel("Analysis Complete!", style="bold green", expand=False))

    except Exception as e:
        console.print(Panel(f"[bold red]Error:[/]\n{str(e)}", title="Error", border_style="red"))
        sys.exit(1)

if __name__ == '__main__':
    main()
