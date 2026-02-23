import sys
import os

# Add the current directory to sys.path to allow imports from local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from crewai import Crew

from agent_config import Config
from agents import BugTriagerAgents
from tasks import BugTriagerTasks
from tools import fetch_open_issues, apply_label, assign_user, post_comment

console = Console()

def main():
    console.print(Panel.fit("[bold blue]Bug Triager Agent[/bold blue]", border_style="blue"))

    try:
        Config.validate()
    except ValueError as e:
        # Check if running in help mode to avoid crashing if env vars are missing
        if len(sys.argv) > 1 and sys.argv[1] == '--help':
            pass
        else:
            console.print(f"[red]Configuration Error: {e}[/red]")
            return

    # Check for CLI args (like --help)
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        console.print("Usage: python main.py")
        console.print("Interactively triages open GitHub issues using AI agents.")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Fetching open issues...", total=None)
        try:
            issues = fetch_open_issues()
            # Access totalCount to trigger the API call and check count
            count = issues.totalCount
            progress.update(task, completed=True)
        except Exception as e:
            console.print(f"[red]Error fetching issues: {e}[/red]")
            return

    if count == 0:
        console.print("[green]No open issues found![/green]")
        return

    console.print(f"[green]Found {count} open issues.[/green]")

    agents = BugTriagerAgents()
    tasks_def = BugTriagerTasks()

    triage_agent = agents.triage_agent()
    duplicate_agent = agents.duplicate_checker_agent()
    response_agent = agents.response_agent()

    for issue in issues:
        console.print(Panel(f"[bold]Issue #{issue.number}: {issue.title}[/bold]\n\n{issue.body[:200]}...", title="Processing Issue", border_style="green"))

        if not Confirm.ask(f"Process Issue #{issue.number}?", default=True):
            continue

        issue_content = f"Title: {issue.title}\nBody: {issue.body}"

        # Define tasks
        analyze_task = tasks_def.analyze_issue_task(triage_agent, issue_content)
        duplicate_task = tasks_def.check_duplicate_task(duplicate_agent, issue_content)
        response_task = tasks_def.draft_response_task(response_agent, issue_content, [analyze_task, duplicate_task])

        crew = Crew(
            agents=[triage_agent, duplicate_agent, response_agent],
            tasks=[analyze_task, duplicate_task, response_task],
            verbose=True
        )

        console.print("[yellow]Running agents...[/yellow]")
        try:
            result = crew.kickoff()
        except Exception as e:
            console.print(f"[red]Error running agents: {e}[/red]")
            continue

        console.print(Panel(Markdown(str(result)), title="Agent Draft Response", border_style="magenta"))

        if Confirm.ask("Do you want to apply actions based on this analysis?"):

            # Label
            label_input = Prompt.ask("Enter label(s) to apply (comma separated, leave empty to skip)")
            if label_input:
                labels = [l.strip() for l in label_input.split(',')]
                for label in labels:
                    if apply_label(issue.number, label):
                        console.print(f"[green]Label '{label}' applied.[/green]")

            # Assign
            assignee = Prompt.ask("Enter username to assign (leave empty to skip)")
            if assignee:
                if assign_user(issue.number, assignee):
                    console.print(f"[green]User '{assignee}' assigned.[/green]")

            # Reply
            if Confirm.ask("Post the drafted reply?"):
                 reply_body = str(result)
                 if post_comment(issue.number, reply_body):
                     console.print("[green]Comment posted.[/green]")

        if not Confirm.ask("Process next issue?", default=True):
            break

if __name__ == "__main__":
    main()
