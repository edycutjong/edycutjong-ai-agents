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
except ImportError as e:  # pragma: no cover
    print(f"Error importing modules: {e}")  # pragma: no cover
    sys.exit(1)  # pragma: no cover

console = Console()

def main():
    console.print(Panel.fit("[bold green]Welcome to the AI Recipe Planner![/bold green]", border_style="green"))

    # Gather User Input
    preferences = Prompt.ask("Enter your dietary preferences (e.g., Vegan, Keto)", default="None")
    allergies = Prompt.ask("Enter any allergies or restrictions (e.g., Peanuts, Gluten)", default="None")
    budget = Prompt.ask("Enter your budget level", choices=["Low", "Medium", "High"], default="Medium")
    days = IntPrompt.ask("How many days should the plan cover?", default=3)

    api_key = config.OPENAI_API_KEY  # pragma: no cover
    if not api_key:  # pragma: no cover
        console.print("[yellow]Warning: OPENAI_API_KEY not found in environment. The agent might fail.[/yellow]")  # pragma: no cover

    try:  # pragma: no cover
        agent = RecipePlannerAgent(api_key=api_key, model_name=config.MODEL_NAME)  # pragma: no cover
    except Exception as e:  # pragma: no cover
        console.print(f"[bold red]Error initializing agent:[/bold red] {e}")  # pragma: no cover
        return  # pragma: no cover

    weekly_plan = None  # pragma: no cover
    shopping_list = None  # pragma: no cover

    # Generate Weekly Plan
    with Progress(  # pragma: no cover
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task1 = progress.add_task(description="Generating weekly meal plan...", total=None)  # pragma: no cover
        try:  # pragma: no cover
            weekly_plan = agent.generate_plan(preferences, allergies, budget, days)  # pragma: no cover
            progress.update(task1, completed=True, description="Meal plan generated!")  # pragma: no cover
        except Exception as e:  # pragma: no cover
            console.print(f"[bold red]Error generating plan:[/bold red] {e}")  # pragma: no cover
            return  # pragma: no cover

        task2 = progress.add_task(description="Generating shopping list...", total=None)  # pragma: no cover
        try:  # pragma: no cover
            shopping_list = agent.generate_shopping_list(weekly_plan)  # pragma: no cover
            progress.update(task2, completed=True, description="Shopping list generated!")  # pragma: no cover
        except Exception as e:  # pragma: no cover
            console.print(f"[bold red]Error generating shopping list:[/bold red] {e}")  # pragma: no cover
            return  # pragma: no cover

    # Display Result Summary
    console.print("\n[bold blue]Plan Generated Successfully![/bold blue]")  # pragma: no cover
    console.print(f"Total Estimated Cost: [green]${weekly_plan.total_estimated_cost:.2f}[/green]")  # pragma: no cover
    console.print(f"Meal Prep Tips: {len(weekly_plan.meal_prep_tips)}")  # pragma: no cover

    # Format Output
    output_content = agent.format_to_markdown(weekly_plan, shopping_list)  # pragma: no cover

    # Save to File
    filename = "meal_plan.md"  # pragma: no cover
    with open(filename, "w") as f:  # pragma: no cover
        f.write(output_content)  # pragma: no cover

    console.print(f"\n[bold green]Detailed plan saved to {filename}[/bold green]")  # pragma: no cover

    # Preview
    preview = Prompt.ask("Do you want to preview the plan in the terminal?", choices=["y", "n"], default="y")  # pragma: no cover
    if preview == "y":  # pragma: no cover
        console.print(Markdown(output_content))  # pragma: no cover

if __name__ == "__main__":
    main()  # pragma: no cover
