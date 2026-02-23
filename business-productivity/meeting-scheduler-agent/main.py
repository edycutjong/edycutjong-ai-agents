import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

# Ensure imports work by adding current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agent.core import create_agent_executor, run_agent_step
except ImportError:
    # If run from root, imports might differ if not handled properly in core.
    # But core handles imports robustly.
    from apps.agents.business_productivity.meeting_scheduler_agent.agent.core import create_agent_executor, run_agent_step

def main():
    console = Console()

    console.print(Panel.fit("[bold blue]Meeting Scheduler Agent[/bold blue]\n[italic]Your AI assistant for finding optimal meeting times.[/italic]", border_style="blue"))

    with console.status("[bold green]Initializing agent...[/bold green]"):
        agent_executor = create_agent_executor()

    if agent_executor is None:
        console.print("[bold red]Error:[/bold red] Agent could not be initialized. Please check your OPENAI_API_KEY in .env.")
        return

    console.print("[green]Agent ready![/green] Type 'exit' or 'quit' to stop.")

    thread_id = "cli_session"

    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")

            if user_input.lower() in ["exit", "quit"]:
                console.print("[bold blue]Goodbye![/bold blue]")
                break

            if not user_input.strip():
                continue

            with console.status("[bold yellow]Agent is thinking...[/bold yellow]"):
                response = run_agent_step(agent_executor, user_input, thread_id=thread_id)

            console.print("\n[bold magenta]Agent[/bold magenta]:")
            console.print(Markdown(str(response)))

        except KeyboardInterrupt:
            console.print("\n[bold blue]Goodbye![/bold blue]")
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()
