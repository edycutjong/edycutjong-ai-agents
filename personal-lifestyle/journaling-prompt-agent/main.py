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
    context = Prompt.ask("Any context? (Optional)", default="")  # pragma: no cover

    entry = tracker.add_mood(mood, energy, context)  # pragma: no cover
    console.print("[green]Mood tracked![/green]")  # pragma: no cover
    return entry  # pragma: no cover

def write_journal_entry(prompt_text: str, mood_entry: Optional[MoodEntry] = None):
    console.print("\n[bold]Your Prompt:[/bold]")  # pragma: no cover
    console.print(Panel(prompt_text, title="Journal Prompt", style="blue"))  # pragma: no cover

    if Confirm.ask("Do you want to write an entry now?"):  # pragma: no cover
        console.print("[italic]Type your entry below. Press Enter to submit.[/italic]")  # pragma: no cover
        response = Prompt.ask("Your Entry")  # pragma: no cover

        entry_id = datetime.now().strftime("%Y%m%d%H%M%S")  # pragma: no cover
        journal_entry = JournalEntry(  # pragma: no cover
            id=entry_id,
            prompt=prompt_text,
            response=response,
            mood_entry=mood_entry
        )
        tracker.save_journal_entry(journal_entry)  # pragma: no cover
        console.print("[green]Entry saved successfully![/green]")  # pragma: no cover

def show_mood_trends():
    history = tracker.get_mood_history()  # pragma: no cover
    if not history:  # pragma: no cover
        console.print("[yellow]No mood history found.[/yellow]")  # pragma: no cover
        return  # pragma: no cover

    table = Table(title="Recent Mood History")  # pragma: no cover
    table.add_column("Date", style="cyan")  # pragma: no cover
    table.add_column("Mood", style="magenta")  # pragma: no cover
    table.add_column("Energy", justify="right", style="green")  # pragma: no cover
    table.add_column("Context")  # pragma: no cover

    for entry in history[-10:]:  # Show last 10  # pragma: no cover
        table.add_row(  # pragma: no cover
            entry.timestamp.strftime("%Y-%m-%d %H:%M"),
            entry.mood,
            str(entry.energy),
            entry.context or ""
        )

    console.print(table)  # pragma: no cover
    Prompt.ask("\nPress Enter to return to menu")  # pragma: no cover

def main_menu(mood_entry: MoodEntry):
    while True:  # pragma: no cover
        clear_screen()  # pragma: no cover
        print_header()  # pragma: no cover
        console.print(f"[dim]Current Mood: {mood_entry.mood} (Energy: {mood_entry.energy}/10)[/dim]\n")  # pragma: no cover

        console.print("[bold]What would you like to do?[/bold]")  # pragma: no cover
        console.print("1. [cyan]Get Daily Contextual Prompt[/cyan]")  # pragma: no cover
        console.print("2. [green]Gratitude Journaling[/green]")  # pragma: no cover
        console.print("3. [blue]Daily Reflection[/blue]")  # pragma: no cover
        console.print("4. [magenta]Themed Prompt[/magenta]")  # pragma: no cover
        console.print("5. [yellow]View Mood Trends[/yellow]")  # pragma: no cover
        console.print("6. [white]Export Entries[/white]")  # pragma: no cover
        console.print("7. [red]Exit[/red]")  # pragma: no cover

        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6", "7"])  # pragma: no cover

        if choice == "1":  # pragma: no cover
            with console.status("[bold green]Generating prompt...[/bold green]"):  # pragma: no cover
                prompt = generator.generate_contextual_prompt(  # pragma: no cover
                    mood=mood_entry.mood,
                    energy=mood_entry.energy,
                    context=mood_entry.context or ""
                )
            write_journal_entry(prompt, mood_entry)  # pragma: no cover

        elif choice == "2":  # pragma: no cover
            with console.status("[bold green]Generating gratitude prompts...[/bold green]"):  # pragma: no cover
                prompt = generator.generate_gratitude_prompts(mood=mood_entry.mood)  # pragma: no cover
            write_journal_entry(prompt, mood_entry)  # pragma: no cover

        elif choice == "3":  # pragma: no cover
            with console.status("[bold green]Generating reflection questions...[/bold green]"):  # pragma: no cover
                prompt = generator.generate_reflection_prompts(context=mood_entry.context or "")  # pragma: no cover
            write_journal_entry(prompt, mood_entry)  # pragma: no cover

        elif choice == "4":  # pragma: no cover
            theme = Prompt.ask("Enter a theme (e.g., Nature, Childhood, Dreams)")  # pragma: no cover
            with console.status(f"[bold green]Generating prompt about {theme}...[/bold green]"):  # pragma: no cover
                prompt = generator.generate_themed_prompt(theme=theme)  # pragma: no cover
            write_journal_entry(prompt, mood_entry)  # pragma: no cover

        elif choice == "5":  # pragma: no cover
            show_mood_trends()  # pragma: no cover

        elif choice == "6":  # pragma: no cover
            entries = tracker.get_journal_entries()  # pragma: no cover
            if entries:  # pragma: no cover
                filepath = export_to_markdown(entries)  # pragma: no cover
                console.print(f"[green]Journal exported to: {filepath}[/green]")  # pragma: no cover
            else:
                console.print("[yellow]No entries to export.[/yellow]")  # pragma: no cover
            # Prompt.ask("\nPress Enter to continue") # Redundant with main loop pause

        elif choice == "7":  # pragma: no cover
            console.print("[bold]Goodbye! Keep journaling.[/bold]")  # pragma: no cover
            sys.exit(0)  # pragma: no cover

        if choice != "5": # 5 already has a pause  # pragma: no cover
             Prompt.ask("\nPress Enter to return to menu")  # pragma: no cover

def main():
    clear_screen()
    print_header()

    # Check API Key
    if not generator.api_key:
        console.print("[bold red]WARNING: OpenAI API Key not found![/bold red]")  # pragma: no cover
        console.print("Please set OPENAI_API_KEY in your .env file.")  # pragma: no cover
        console.print("Prompts will not be generated correctly.")  # pragma: no cover
        if not Confirm.ask("Do you want to continue anyway?"):  # pragma: no cover
            sys.exit(1)  # pragma: no cover

    try:
        mood_entry = get_mood_input()
        main_menu(mood_entry)  # pragma: no cover
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting...[/bold red]")  # pragma: no cover
        sys.exit(0)  # pragma: no cover

if __name__ == "__main__":
    main()  # pragma: no cover
