import os
import sys

# Ensure correct path to allow imports from agent and prompts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from agent.models import UserProfile
from agent.generator import generate_workout_plan
from agent.exporter import export_to_markdown, export_to_pdf
from config import OPENAI_API_KEY

def main():
    console = Console()

    console.print(Panel.fit("[bold cyan]AI Workout Planner[/bold cyan]", border_style="cyan"))
    console.print("[dim]Create a personalized workout plan tailored to your goals.[/dim]\n")

    # Check for API Key but don't crash if strictly testing without one (though generation will fail)
    if not OPENAI_API_KEY:
        console.print("[bold yellow]Warning:[/bold yellow] OPENAI_API_KEY not found in .env. Generation will likely fail.")  # pragma: no cover

    try:
        # User Input
        name = Prompt.ask("What is your [bold]name[/bold]?")
        age = IntPrompt.ask("What is your [bold]age[/bold]?", default=30)
        weight = FloatPrompt.ask("What is your [bold]weight (kg)[/bold]?", default=70.0)  # pragma: no cover
        height = FloatPrompt.ask("What is your [bold]height (cm)[/bold]?", default=175.0)  # pragma: no cover

        fitness_goal = Prompt.ask(  # pragma: no cover
            "What is your [bold]fitness goal[/bold]?",
            choices=["Weight Loss", "Muscle Gain", "Endurance", "Flexibility", "General Health"],
            default="General Health"
        )

        fitness_level = Prompt.ask(  # pragma: no cover
            "What is your [bold]current fitness level[/bold]?",
            choices=["Beginner", "Intermediate", "Advanced"],
            default="Intermediate"
        )

        equipment_input = Prompt.ask("What [bold]equipment[/bold] do you have available? (comma separated, or 'None')")  # pragma: no cover
        # Handle 'None' explicitly, strip spaces, ignore empty strings
        if equipment_input.lower() == 'none' or not equipment_input.strip():  # pragma: no cover
            equipment = []  # pragma: no cover
        else:
            equipment = [e.strip() for e in equipment_input.split(',') if e.strip()]  # pragma: no cover

        days_per_week = IntPrompt.ask("How many [bold]days per week[/bold] can you workout?", default=3)  # pragma: no cover
        duration_per_session = IntPrompt.ask("How many [bold]minutes per session[/bold]?", default=45)  # pragma: no cover

        user_profile = UserProfile(  # pragma: no cover
            name=name,
            age=age,
            weight=weight,
            height=height,
            fitness_goal=fitness_goal,
            fitness_level=fitness_level,
            equipment=equipment,
            days_per_week=days_per_week,
            duration_per_session=duration_per_session
        )

        console.print("\n[bold green]Generating your workout plan...[/bold green]")  # pragma: no cover

        plan = None  # pragma: no cover
        with Progress(  # pragma: no cover
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Thinking...", total=None)  # pragma: no cover
            try:  # pragma: no cover
                plan = generate_workout_plan(user_profile)  # pragma: no cover
            except Exception as e:  # pragma: no cover
                console.print(f"[bold red]Error generating plan:[/bold red] {e}")  # pragma: no cover
                return  # pragma: no cover

        if not plan:  # pragma: no cover
            console.print("[bold red]Failed to generate plan.[/bold red]")  # pragma: no cover
            return  # pragma: no cover

        console.print(Panel(f"[bold]{plan.plan_name}[/bold]\n\n{plan.difficulty_progression}", title="Plan Overview", border_style="green"))  # pragma: no cover

        # Display preview (just the first week)
        if plan.weeks:  # pragma: no cover
            week1 = plan.weeks[0]  # pragma: no cover
            console.print(f"\n[bold underline]Week {week1.week_number}: {week1.focus}[/bold underline]")  # pragma: no cover
            for session in week1.sessions:  # pragma: no cover
                console.print(f"- [cyan]{session.day}[/cyan]: {session.workout_type} ({session.duration_minutes} min)")  # pragma: no cover

        console.print("\n[dim]...Full plan generated.[/dim]\n")  # pragma: no cover

        # Export options
        save_md = Prompt.ask("Save as Markdown?", choices=["y", "n"], default="y")  # pragma: no cover
        if save_md == "y":  # pragma: no cover
            filename = Prompt.ask("Filename", default="workout_plan.md")  # pragma: no cover
            export_to_markdown(plan, filename)  # pragma: no cover
            console.print(f"[green]Saved to {filename}[/green]")  # pragma: no cover

        save_pdf = Prompt.ask("Save as PDF?", choices=["y", "n"], default="n")  # pragma: no cover
        if save_pdf == "y":  # pragma: no cover
            filename = Prompt.ask("Filename", default="workout_plan.pdf")  # pragma: no cover
            export_to_pdf(plan, filename)  # pragma: no cover
            console.print(f"[green]Saved to {filename}[/green]")  # pragma: no cover

        console.print("\n[bold cyan]Enjoy your workout![/bold cyan]")  # pragma: no cover

    except KeyboardInterrupt:
        console.print("\n[bold red]Cancelled.[/bold red]")  # pragma: no cover
        return  # pragma: no cover

if __name__ == "__main__":
    main()  # pragma: no cover
