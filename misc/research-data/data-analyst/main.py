import os
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from dotenv import load_dotenv

# Add current directory to path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_config import create_agent

load_dotenv()

console = Console()

def load_data(filepath: str) -> pd.DataFrame:
    """Loads CSV or Excel file into a pandas DataFrame."""
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(filepath)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel.")
        return df
    except Exception as e:
        console.print(f"[bold red]Error loading file:[/bold red] {e}")
        return None

def show_summary(df: pd.DataFrame):
    """Displays a summary of the DataFrame using Rich tables."""
    if df is None:
        return

    console.print(Panel(Text("Data Summary", justify="center", style="bold white"), style="bold blue"))

    # Create a table for general info
    table = Table(title="DataFrame Overview", show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Property", style="dim", width=20)
    table.add_column("Value")

    table.add_row("Rows", str(df.shape[0]))
    table.add_row("Columns", str(df.shape[1]))
    table.add_row("Missing Values", str(df.isnull().sum().sum()))

    console.print(table)

    # Create a table for column details
    col_table = Table(title="Column Details", show_header=True, header_style="bold cyan", expand=True)
    col_table.add_column("Column Name", style="bold")
    col_table.add_column("Type")
    col_table.add_column("Unique Values")
    col_table.add_column("Example (First Row)")

    for col in df.columns:
        example = str(df[col].iloc[0]) if not df.empty else "N/A"
        col_table.add_row(
            col,
            str(df[col].dtype),
            str(df[col].nunique()),
            example
        )

    console.print(col_table)

    # Show head
    head_table = Table(title="First 5 Rows", show_header=True, header_style="bold green", expand=True)
    for col in df.columns:
        head_table.add_column(col)

    for i in range(min(5, len(df))):
        row = [str(x) for x in df.iloc[i]]
        head_table.add_row(*row)

    console.print(head_table)

def export_report(history):
    """Exports the conversation history to a markdown file."""
    filename = "analysis_report.md"
    with open(filename, "w") as f:
        f.write("# Data Analysis Report\n\n")
        for q, a in history:
            f.write(f"## Question: {q}\n\n")
            f.write(f"**Answer:**\n{a}\n\n")
            f.write("---\n\n")
    console.print(f"[bold green]Report exported to {filename}[/bold green]")

def main():
    console.print(Panel.fit(
        "[bold cyan]AI Data Analyst[/bold cyan]\n[dim]Analyze CSV/Excel files with natural language[/dim]",
        border_style="blue"
    ))

    # Ask for file path, default to data.csv if exists
    default_file = "data.csv" if os.path.exists("data.csv") else "apps/agents/data-analyst/data.csv"
    if not os.path.exists(default_file):
        default_file = "" # Prompt for it if default not found

    filepath = Prompt.ask("Enter path to CSV/Excel file", default=default_file)

    if not os.path.exists(filepath):
        console.print(f"[bold red]File not found:[/bold red] {filepath}")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Loading data...", total=None)
        df = load_data(filepath)

    if df is None:
        return

    show_summary(df)

    # Initialize Agent
    console.print(Panel("Initializing AI Agent...", style="yellow"))
    try:
        agent = create_agent(df)
    except Exception as e:
         console.print(f"[bold red]Error initializing agent:[/bold red] {e}")
         return

    console.print("[bold green]Agent ready! Ask questions about your data. Type 'exit' to quit or 'export' to save report.[/bold green]")

    history = []

    while True:
        user_input = Prompt.ask("\n[bold cyan]Query[/bold cyan]")

        if user_input.lower() in ['exit', 'quit']:
            break

        if user_input.lower() == 'export':
            export_report(history)
            continue

        if not user_input.strip():
            continue

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Analyzing...", total=None)
            try:
                # AgentExecutor invoke method
                result = agent.invoke({"input": user_input})
                response = result.get("output", str(result))
            except Exception as e:
                response = f"Error: {str(e)}"

        console.print(Panel(Markdown(response), title="AI Response", border_style="green"))
        history.append((user_input, response))

    console.print("[bold blue]Goodbye![/bold blue]")

if __name__ == "__main__":
    main()
