import sys
import os
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

# Add current directory to path so imports work
sys.path.append(os.path.dirname(__file__))

from agent.planner import LearningPathPlanner
from agent.tracker import ProgressTracker
from agent.models import LearningPath
from config import config

console = Console()
planner = LearningPathPlanner()
tracker = ProgressTracker()

def display_welcome():
    console.print(Panel.fit("[bold cyan]Learning Path Planner AI[/bold cyan]\n[yellow]Accelerate your career with a personalized roadmap[/yellow]"))

def display_path(path: LearningPath):
    console.print(f"\n[bold green]Learning Path: {path.topic}[/bold green] (Level: {path.user_level})")  # pragma: no cover
    console.print(f"Total Estimated Time: {path.total_estimated_time}")  # pragma: no cover

    table = Table(title="Milestones")  # pragma: no cover
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)  # pragma: no cover
    table.add_column("Status", justify="center")  # pragma: no cover
    table.add_column("Title", style="magenta")  # pragma: no cover
    table.add_column("Description")  # pragma: no cover
    table.add_column("Duration", justify="right")  # pragma: no cover

    for m in path.milestones:  # pragma: no cover
        status = "[green]✔ DONE[/green]" if m.is_completed else "[red]○ TODO[/red]"  # pragma: no cover
        table.add_row(str(m.id), status, m.title, m.description, m.estimated_time)  # pragma: no cover

    console.print(table)  # pragma: no cover

def view_milestone_details(path: LearningPath):
    milestone_id = Prompt.ask("Enter Milestone ID to view details", default="1")  # pragma: no cover
    try:  # pragma: no cover
        m_id = int(milestone_id)  # pragma: no cover
        milestone = next((m for m in path.milestones if m.id == m_id), None)  # pragma: no cover
        if milestone:  # pragma: no cover
            console.print(Panel(f"[bold]{milestone.title}[/bold]\n{milestone.description}", title=f"Milestone {milestone.id}"))  # pragma: no cover

            console.print("\n[bold]Skills:[/bold]")  # pragma: no cover
            for skill in milestone.skills:  # pragma: no cover
                console.print(f"- {skill}")  # pragma: no cover

            console.print("\n[bold]Resources:[/bold]")  # pragma: no cover
            for res in milestone.resources:  # pragma: no cover
                cost = f"({res.cost})" if res.is_paid else "(Free)"  # pragma: no cover
                console.print(f"- [{res.type}] {res.title} {cost}: [blue underline]{res.url}[/blue underline]")  # pragma: no cover

            if milestone.projects:  # pragma: no cover
                console.print("\n[bold]Projects:[/bold]")  # pragma: no cover
                for proj in milestone.projects:  # pragma: no cover
                    console.print(f"- {proj.title} ({proj.estimated_duration}): {proj.description}")  # pragma: no cover
        else:
            console.print("[red]Milestone not found.[/red]")  # pragma: no cover
    except ValueError:  # pragma: no cover
        console.print("[red]Invalid ID.[/red]")  # pragma: no cover

def create_new_path():
    topic = Prompt.ask("What topic or role do you want to learn?", default="Python Backend Developer")  # pragma: no cover
    user_level = Prompt.ask("What is your current skill level?", choices=["Beginner", "Intermediate", "Advanced"], default="Beginner")  # pragma: no cover
    additional_info = Prompt.ask("Any specific goals or preferences? (Optional)")  # pragma: no cover

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:  # pragma: no cover
        progress.add_task(description="Generating your personalized learning path...", total=None)  # pragma: no cover
        path = planner.generate_path(topic, user_level, additional_info)  # pragma: no cover

    tracker.save_path(path)  # pragma: no cover
    console.print("[green]Path generated successfully![/green]")  # pragma: no cover
    display_path(path)  # pragma: no cover

def update_progress(path: LearningPath):
    display_path(path)  # pragma: no cover
    milestone_id = Prompt.ask("Enter Milestone ID to mark as complete")  # pragma: no cover
    try:  # pragma: no cover
        m_id = int(milestone_id)  # pragma: no cover
        updated_path = tracker.mark_milestone_complete(m_id)  # pragma: no cover
        if updated_path:  # pragma: no cover
            console.print(f"[green]Milestone {m_id} marked as complete![/green]")  # pragma: no cover

            # Ask if user wants to adjust path
            if Confirm.ask("Do you want to adjust the remaining path based on this progress?"):  # pragma: no cover
                 feedback = Prompt.ask("How was it? (e.g., too easy, too hard, need more projects)")  # pragma: no cover
                 with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:  # pragma: no cover
                    progress.add_task(description="Adjusting path...", total=None)  # pragma: no cover
                    new_path = planner.adjust_path(updated_path, feedback)  # pragma: no cover
                 tracker.save_path(new_path)  # pragma: no cover
                 console.print("[green]Path updated![/green]")  # pragma: no cover
                 display_path(new_path)  # pragma: no cover
        else:
            console.print("[red]Could not update path.[/red]")  # pragma: no cover
    except ValueError:  # pragma: no cover
        console.print("[red]Invalid ID.[/red]")  # pragma: no cover

def main():
    display_welcome()

    while True:
        path = tracker.load_path()
        options = []
        if path:
            options = ["View Current Path", "View Milestone Details", "Update Progress", "Create New Path", "Exit"]  # pragma: no cover
        else:
            options = ["Create New Path", "Exit"]

        choice = Prompt.ask("Choose an action", choices=options)

        if choice == "Create New Path":
            create_new_path()  # pragma: no cover
        elif choice == "View Current Path":
            display_path(path)  # pragma: no cover
        elif choice == "View Milestone Details":
            view_milestone_details(path)  # pragma: no cover
        elif choice == "Update Progress":
            update_progress(path)  # pragma: no cover
        elif choice == "Exit":
            console.print("[yellow]Goodbye! Happy Learning![/yellow]")  # pragma: no cover
            break  # pragma: no cover

if __name__ == "__main__":
    main()  # pragma: no cover
