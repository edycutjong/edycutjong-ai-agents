#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text

# Add src to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.append(src_dir)

from git_utils import get_commits, format_commits_for_agent
from agents import ChangelogAgents
from tasks import ChangelogTasks
from crewai import Crew

load_dotenv()

console = Console()

def main():
    console.clear()
    console.print(Panel.fit(
        Text("AI Changelog Writer", style="bold magenta", justify="center"),
        subtitle="Powered by CrewAI",
        border_style="cyan"
    ))

    repo_path = Prompt.ask("Repository Path", default=os.getcwd())
    from_ref = Prompt.ask("From Ref (e.g. tag, hash, HEAD~5)", default="HEAD~10")
    to_ref = Prompt.ask("To Ref", default="HEAD")

    commits = []
    formatted_commits = ""

    with console.status("[bold green]Fetching git commits...", spinner="dots"):
        try:
            commits = get_commits(repo_path, from_ref, to_ref)
            formatted_commits = format_commits_for_agent(commits)
            console.print(f"[green]✓ Found {len(commits)} commits.[/green]")
        except Exception as e:
            console.print(f"[bold red]Error fetching commits:[/bold red] {e}")
            return

    if not commits:
        console.print("[yellow]No commits found in the specified range.[/yellow]")
        return

    agents = ChangelogAgents()
    tasks = ChangelogTasks()

    # Initialize Agents
    classifier_agent = agents.commit_classifier()
    writer_agent = agents.changelog_writer()

    # Initialize Tasks
    classify_task = tasks.classify_commits_task(classifier_agent, formatted_commits)
    write_task = tasks.write_changelog_task(writer_agent)

    # Context is handled automatically by CrewAI when tasks are in order
    # Specifically, the output of classify_task will be available to write_task
    # We might need to explicitly link context if we want to be sure, but linear process works by default.
    # To be safe in newer versions, we can pass context=[classify_task] to write_task but
    # the method in tasks.py doesn't accept it currently. Let's rely on default sequential execution.

    crew = Crew(
        agents=[classifier_agent, writer_agent],
        tasks=[classify_task, write_task],
        verbose=True
    )

    console.print(Panel("Starting AI Agents...", style="yellow"))

    try:
        result = crew.kickoff()
    except Exception as e:
        console.print(f"[bold red]Error running agents:[/bold red] {e}")
        return

    # Check if result is a string or a TaskOutput object
    final_output = result
    if hasattr(result, 'raw'):
        final_output = result.raw

    console.print(Panel(Markdown(str(final_output)), title="Generated Changelog", border_style="green"))

    output_file = "CHANGELOG.md"
    try:
        with open(output_file, "w") as f:
            f.write(str(final_output))
        console.print(f"[bold blue]Changelog saved to {output_file}[/bold blue]")
    except IOError as e:
         console.print(f"[bold red]Error saving file:[/bold red] {e}")

if __name__ == "__main__":
    main()
