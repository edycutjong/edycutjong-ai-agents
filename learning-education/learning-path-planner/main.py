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
    console.print(f"\n[bold green]Learning Path: {path.topic}[/bold green] (Level: {path.user_level})")
    console.print(f"Total Estimated Time: {path.total_estimated_time}")

    table = Table(title="Milestones")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Title", style="magenta")
    table.add_column("Description")
    table.add_column("Duration", justify="right")

    for m in path.milestones:
        status = "[green]✔ DONE[/green]" if m.is_completed else "[red]○ TODO[/red]"
        table.add_row(str(m.id), status, m.title, m.description, m.estimated_time)

    console.print(table)

def view_milestone_details(path: LearningPath):
    milestone_id = Prompt.ask("Enter Milestone ID to view details", default="1")
    try:
        m_id = int(milestone_id)
        milestone = next((m for m in path.milestones if m.id == m_id), None)
        if milestone:
            console.print(Panel(f"[bold]{milestone.title}[/bold]\n{milestone.description}", title=f"Milestone {milestone.id}"))

            console.print("\n[bold]Skills:[/bold]")
            for skill in milestone.skills:
                console.print(f"- {skill}")

            console.print("\n[bold]Resources:[/bold]")
            for res in milestone.resources:
                cost = f"({res.cost})" if res.is_paid else "(Free)"
                console.print(f"- [{res.type}] {res.title} {cost}: [blue underline]{res.url}[/blue underline]")

            if milestone.projects:
                console.print("\n[bold]Projects:[/bold]")
                for proj in milestone.projects:
                    console.print(f"- {proj.title} ({proj.estimated_duration}): {proj.description}")
        else:
            console.print("[red]Milestone not found.[/red]")
    except ValueError:
        console.print("[red]Invalid ID.[/red]")

def create_new_path():
    topic = Prompt.ask("What topic or role do you want to learn?", default="Python Backend Developer")
    user_level = Prompt.ask("What is your current skill level?", choices=["Beginner", "Intermediate", "Advanced"], default="Beginner")
    additional_info = Prompt.ask("Any specific goals or preferences? (Optional)")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Generating your personalized learning path...", total=None)
        path = planner.generate_path(topic, user_level, additional_info)

    tracker.save_path(path)
    console.print("[green]Path generated successfully![/green]")
    display_path(path)

def update_progress(path: LearningPath):
    display_path(path)
    milestone_id = Prompt.ask("Enter Milestone ID to mark as complete")
    try:
        m_id = int(milestone_id)
        updated_path = tracker.mark_milestone_complete(m_id)
        if updated_path:
            console.print(f"[green]Milestone {m_id} marked as complete![/green]")

            # Ask if user wants to adjust path
            if Confirm.ask("Do you want to adjust the remaining path based on this progress?"):
                 feedback = Prompt.ask("How was it? (e.g., too easy, too hard, need more projects)")
                 with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
                    progress.add_task(description="Adjusting path...", total=None)
                    new_path = planner.adjust_path(updated_path, feedback)
                 tracker.save_path(new_path)
                 console.print("[green]Path updated![/green]")
                 display_path(new_path)
        else:
            console.print("[red]Could not update path.[/red]")
    except ValueError:
        console.print("[red]Invalid ID.[/red]")

def main():
    display_welcome()

    while True:
        path = tracker.load_path()
        options = []
        if path:
            options = ["View Current Path", "View Milestone Details", "Update Progress", "Create New Path", "Exit"]
        else:
            options = ["Create New Path", "Exit"]

        choice = Prompt.ask("Choose an action", choices=options)

        if choice == "Create New Path":
            create_new_path()
        elif choice == "View Current Path":
            display_path(path)
        elif choice == "View Milestone Details":
            view_milestone_details(path)
        elif choice == "Update Progress":
            update_progress(path)
        elif choice == "Exit":
            console.print("[yellow]Goodbye! Happy Learning![/yellow]")
            break

if __name__ == "__main__":
    main()
