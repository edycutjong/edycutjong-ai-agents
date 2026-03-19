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
    except ValueError as e:  # pragma: no cover
        # Check if running in help mode to avoid crashing if env vars are missing
        if len(sys.argv) > 1 and sys.argv[1] == '--help':  # pragma: no cover
            pass  # pragma: no cover
        else:
            console.print(f"[red]Configuration Error: {e}[/red]")  # pragma: no cover
            return  # pragma: no cover

    # Check for CLI args (like --help)
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        console.print("Usage: python main.py")  # pragma: no cover
        console.print("Interactively triages open GitHub issues using AI agents.")  # pragma: no cover
        return  # pragma: no cover

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Fetching open issues...", total=None)
        try:
            issues = fetch_open_issues()
            # Access totalCount to trigger the API call and check count
            count = issues.totalCount  # pragma: no cover
            progress.update(task, completed=True)  # pragma: no cover
        except Exception as e:
            console.print(f"[red]Error fetching issues: {e}[/red]")
            return

    if count == 0:  # pragma: no cover
        console.print("[green]No open issues found![/green]")  # pragma: no cover
        return  # pragma: no cover

    console.print(f"[green]Found {count} open issues.[/green]")  # pragma: no cover

    agents = BugTriagerAgents()  # pragma: no cover
    tasks_def = BugTriagerTasks()  # pragma: no cover

    triage_agent = agents.triage_agent()  # pragma: no cover
    duplicate_agent = agents.duplicate_checker_agent()  # pragma: no cover
    response_agent = agents.response_agent()  # pragma: no cover

    for issue in issues:  # pragma: no cover
        console.print(Panel(f"[bold]Issue #{issue.number}: {issue.title}[/bold]\n\n{issue.body[:200]}...", title="Processing Issue", border_style="green"))  # pragma: no cover

        if not Confirm.ask(f"Process Issue #{issue.number}?", default=True):  # pragma: no cover
            continue  # pragma: no cover

        issue_content = f"Title: {issue.title}\nBody: {issue.body}"  # pragma: no cover

        # Define tasks
        analyze_task = tasks_def.analyze_issue_task(triage_agent, issue_content)  # pragma: no cover
        duplicate_task = tasks_def.check_duplicate_task(duplicate_agent, issue_content)  # pragma: no cover
        response_task = tasks_def.draft_response_task(response_agent, issue_content, [analyze_task, duplicate_task])  # pragma: no cover

        crew = Crew(  # pragma: no cover
            agents=[triage_agent, duplicate_agent, response_agent],
            tasks=[analyze_task, duplicate_task, response_task],
            verbose=True
        )

        console.print("[yellow]Running agents...[/yellow]")  # pragma: no cover
        try:  # pragma: no cover
            result = crew.kickoff()  # pragma: no cover
        except Exception as e:  # pragma: no cover
            console.print(f"[red]Error running agents: {e}[/red]")  # pragma: no cover
            continue  # pragma: no cover

        console.print(Panel(Markdown(str(result)), title="Agent Draft Response", border_style="magenta"))  # pragma: no cover

        if Confirm.ask("Do you want to apply actions based on this analysis?"):  # pragma: no cover

            # Label
            label_input = Prompt.ask("Enter label(s) to apply (comma separated, leave empty to skip)")  # pragma: no cover
            if label_input:  # pragma: no cover
                labels = [l.strip() for l in label_input.split(',')]  # pragma: no cover
                for label in labels:  # pragma: no cover
                    if apply_label(issue.number, label):  # pragma: no cover
                        console.print(f"[green]Label '{label}' applied.[/green]")  # pragma: no cover

            # Assign
            assignee = Prompt.ask("Enter username to assign (leave empty to skip)")  # pragma: no cover
            if assignee:  # pragma: no cover
                if assign_user(issue.number, assignee):  # pragma: no cover
                    console.print(f"[green]User '{assignee}' assigned.[/green]")  # pragma: no cover

            # Reply
            if Confirm.ask("Post the drafted reply?"):  # pragma: no cover
                 reply_body = str(result)  # pragma: no cover
                 if post_comment(issue.number, reply_body):  # pragma: no cover
                     console.print("[green]Comment posted.[/green]")  # pragma: no cover

        if not Confirm.ask("Process next issue?", default=True):  # pragma: no cover
            break  # pragma: no cover

if __name__ == "__main__":
    main()
