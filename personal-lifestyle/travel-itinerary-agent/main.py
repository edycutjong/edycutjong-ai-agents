import os
import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.markdown import Markdown
from fpdf import FPDF
from agent.core import TravelAgent

console = Console()

def export_to_markdown(content: str, filename: str = "itinerary.md"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"[green]Successfully saved Markdown itinerary to {filename}[/green]")
    except Exception as e:
        console.print(f"[red]Error saving Markdown: {e}[/red]")

def export_to_pdf(content: str, filename: str = "itinerary.pdf"):
    try:
        pdf = FPDF()
        pdf.add_page()
        # Use a standard font. For full unicode support (emojis), a TTF font is required.
        # Since we don't have one bundled, we'll stick to standard fonts and handle encoding gracefully.
        pdf.set_font("Helvetica", size=12)

        # Split lines to manage layout
        for line in content.split('\n'):
            # Replace unsupported characters to prevent crashes with standard fonts
            # This will replace emojis with '?' or similar, but is safe.
            safe_line = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, text=safe_line)

        pdf.output(filename)
        console.print(f"[green]Successfully saved PDF itinerary to {filename}[/green]")
    except Exception as e:
        console.print(f"[red]Error saving PDF: {e}[/red]")

def main():
    console.print("[bold blue]Welcome to the AI Travel Itinerary Planner![/bold blue]")
    console.print("Let's plan your perfect trip.\n")

    destination = Prompt.ask("[bold green]Where would you like to go?[/bold green]")
    dates = Prompt.ask("[bold green]When are you planning to travel?[/bold green] (e.g., May 10-20, 2024)")

    console.print(f"\n[bold yellow]Generating itinerary for {destination} ({dates})...[/bold yellow]")

    with console.status("[bold green]Agent is researching and planning...[/bold green]", spinner="dots"):
        agent = TravelAgent()
        if not agent.llm:
            console.print("[bold red]Error: OPENAI_API_KEY is missing. Please check your .env file.[/bold red]")
            return

        itinerary = agent.generate_itinerary(destination, dates)

    console.print("\n[bold blue]Your Itinerary:[/bold blue]\n")
    console.print(Markdown(itinerary))

    if Prompt.ask("\n[bold cyan]Would you like to save this itinerary?[/bold cyan]", choices=["y", "n"], default="y") == "y":
        export_to_markdown(itinerary)
        export_to_pdf(itinerary)

if __name__ == "__main__":
    main()
