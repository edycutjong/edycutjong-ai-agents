import os
import sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add the project root to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config import config
    from agent.planner import RecipePlannerAgent
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

console = Console()

def main():
    console.print(Panel.fit("[bold green]Welcome to the AI Recipe Planner![/bold green]", border_style="green"))

    # Gather User Input
    preferences = Prompt.ask("Enter your dietary preferences (e.g., Vegan, Keto)", default="None")
    allergies = Prompt.ask("Enter any allergies or restrictions (e.g., Peanuts, Gluten)", default="None")
    budget = Prompt.ask("Enter your budget level", choices=["Low", "Medium", "High"], default="Medium")
    days = IntPrompt.ask("How many days should the plan cover?", default=3)

    api_key = config.OPENAI_API_KEY
    if not api_key:
        console.print("[yellow]Warning: OPENAI_API_KEY not found in environment. The agent might fail.[/yellow]")

    try:
        agent = RecipePlannerAgent(api_key=api_key, model_name=config.MODEL_NAME)
    except Exception as e:
        console.print(f"[bold red]Error initializing agent:[/bold red] {e}")
        return

    weekly_plan = None
    shopping_list = None

    # Generate Weekly Plan
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task1 = progress.add_task(description="Generating weekly meal plan...", total=None)
        try:
            weekly_plan = agent.generate_plan(preferences, allergies, budget, days)
            progress.update(task1, completed=True, description="Meal plan generated!")
        except Exception as e:
            console.print(f"[bold red]Error generating plan:[/bold red] {e}")
            return

        task2 = progress.add_task(description="Generating shopping list...", total=None)
        try:
            shopping_list = agent.generate_shopping_list(weekly_plan)
            progress.update(task2, completed=True, description="Shopping list generated!")
        except Exception as e:
            console.print(f"[bold red]Error generating shopping list:[/bold red] {e}")
            return

    # Display Result Summary
    console.print("\n[bold blue]Plan Generated Successfully![/bold blue]")
    console.print(f"Total Estimated Cost: [green]${weekly_plan.total_estimated_cost:.2f}[/green]")
    console.print(f"Meal Prep Tips: {len(weekly_plan.meal_prep_tips)}")

    # Format Output
    output_content = agent.format_to_markdown(weekly_plan, shopping_list)

    # Save to File
    filename = "meal_plan.md"
    with open(filename, "w") as f:
        f.write(output_content)

    console.print(f"\n[bold green]Detailed plan saved to {filename}[/bold green]")

    # Preview
    preview = Prompt.ask("Do you want to preview the plan in the terminal?", choices=["y", "n"], default="y")
    if preview == "y":
        console.print(Markdown(output_content))

if __name__ == "__main__":
    main()
