import sys
from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.markdown import Markdown
from rich.table import Table
from rich import print as rprint

from agent.tracker import Tracker, MoodEntry, JournalEntry
from agent.generator import PromptGenerator
from agent.exporter import export_to_markdown

console = Console()
tracker = Tracker()
generator = PromptGenerator()

def clear_screen():
    console.clear()

def print_header():
    console.print(Panel.fit(
        "[bold magenta]Journaling Prompt Agent[/bold magenta]\n"
        "[italic cyan]Your personal AI journaling companion[/italic cyan]",
        subtitle="v1.0"
    ))

def get_mood_input() -> MoodEntry:
    console.print("\n[bold]How are you feeling right now?[/bold]")
    mood = Prompt.ask("Mood (e.g., Happy, Anxious, Calm)")
    energy = IntPrompt.ask("Energy Level (1-10)", choices=[str(i) for i in range(1, 11)])
    context = Prompt.ask("Any context? (Optional)", default="")

    entry = tracker.add_mood(mood, energy, context)
    console.print("[green]Mood tracked![/green]")
    return entry

def write_journal_entry(prompt_text: str, mood_entry: Optional[MoodEntry] = None):
    console.print("\n[bold]Your Prompt:[/bold]")
    console.print(Panel(prompt_text, title="Journal Prompt", style="blue"))

    if Confirm.ask("Do you want to write an entry now?"):
        console.print("[italic]Type your entry below. Press Enter to submit.[/italic]")
        response = Prompt.ask("Your Entry")

        entry_id = datetime.now().strftime("%Y%m%d%H%M%S")
        journal_entry = JournalEntry(
            id=entry_id,
            prompt=prompt_text,
            response=response,
            mood_entry=mood_entry
        )
        tracker.save_journal_entry(journal_entry)
        console.print("[green]Entry saved successfully![/green]")

def show_mood_trends():
    history = tracker.get_mood_history()
    if not history:
        console.print("[yellow]No mood history found.[/yellow]")
        return

    table = Table(title="Recent Mood History")
    table.add_column("Date", style="cyan")
    table.add_column("Mood", style="magenta")
    table.add_column("Energy", justify="right", style="green")
    table.add_column("Context")

    for entry in history[-10:]:  # Show last 10
        table.add_row(
            entry.timestamp.strftime("%Y-%m-%d %H:%M"),
            entry.mood,
            str(entry.energy),
            entry.context or ""
        )

    console.print(table)
    Prompt.ask("\nPress Enter to return to menu")

def main_menu(mood_entry: MoodEntry):
    while True:
        clear_screen()
        print_header()
        console.print(f"[dim]Current Mood: {mood_entry.mood} (Energy: {mood_entry.energy}/10)[/dim]\n")

        console.print("[bold]What would you like to do?[/bold]")
        console.print("1. [cyan]Get Daily Contextual Prompt[/cyan]")
        console.print("2. [green]Gratitude Journaling[/green]")
        console.print("3. [blue]Daily Reflection[/blue]")
        console.print("4. [magenta]Themed Prompt[/magenta]")
        console.print("5. [yellow]View Mood Trends[/yellow]")
        console.print("6. [white]Export Entries[/white]")
        console.print("7. [red]Exit[/red]")

        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6", "7"])

        if choice == "1":
            with console.status("[bold green]Generating prompt...[/bold green]"):
                prompt = generator.generate_contextual_prompt(
                    mood=mood_entry.mood,
                    energy=mood_entry.energy,
                    context=mood_entry.context or ""
                )
            write_journal_entry(prompt, mood_entry)

        elif choice == "2":
            with console.status("[bold green]Generating gratitude prompts...[/bold green]"):
                prompt = generator.generate_gratitude_prompts(mood=mood_entry.mood)
            write_journal_entry(prompt, mood_entry)

        elif choice == "3":
            with console.status("[bold green]Generating reflection questions...[/bold green]"):
                prompt = generator.generate_reflection_prompts(context=mood_entry.context or "")
            write_journal_entry(prompt, mood_entry)

        elif choice == "4":
            theme = Prompt.ask("Enter a theme (e.g., Nature, Childhood, Dreams)")
            with console.status(f"[bold green]Generating prompt about {theme}...[/bold green]"):
                prompt = generator.generate_themed_prompt(theme=theme)
            write_journal_entry(prompt, mood_entry)

        elif choice == "5":
            show_mood_trends()

        elif choice == "6":
            entries = tracker.get_journal_entries()
            if entries:
                filepath = export_to_markdown(entries)
                console.print(f"[green]Journal exported to: {filepath}[/green]")
            else:
                console.print("[yellow]No entries to export.[/yellow]")
            # Prompt.ask("\nPress Enter to continue") # Redundant with main loop pause

        elif choice == "7":
            console.print("[bold]Goodbye! Keep journaling.[/bold]")
            sys.exit(0)

        if choice != "5": # 5 already has a pause
             Prompt.ask("\nPress Enter to return to menu")

def main():
    clear_screen()
    print_header()

    # Check API Key
    if not generator.api_key:
        console.print("[bold red]WARNING: OpenAI API Key not found![/bold red]")
        console.print("Please set OPENAI_API_KEY in your .env file.")
        console.print("Prompts will not be generated correctly.")
        if not Confirm.ask("Do you want to continue anyway?"):
            sys.exit(1)

    try:
        mood_entry = get_mood_input()
        main_menu(mood_entry)
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting...[/bold red]")
        sys.exit(0)

if __name__ == "__main__":
    main()
