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
            df = pd.read_excel(filepath)  # pragma: no cover
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel.")
        return df
    except Exception as e:
        console.print(f"[bold red]Error loading file:[/bold red] {e}")
        return None

def show_summary(df: pd.DataFrame):
    """Displays a summary of the DataFrame using Rich tables."""
    if df is None:  # pragma: no cover
        return  # pragma: no cover

    console.print(Panel(Text("Data Summary", justify="center", style="bold white"), style="bold blue"))  # pragma: no cover

    # Create a table for general info
    table = Table(title="DataFrame Overview", show_header=True, header_style="bold magenta", expand=True)  # pragma: no cover
    table.add_column("Property", style="dim", width=20)  # pragma: no cover
    table.add_column("Value")  # pragma: no cover

    table.add_row("Rows", str(df.shape[0]))  # pragma: no cover
    table.add_row("Columns", str(df.shape[1]))  # pragma: no cover
    table.add_row("Missing Values", str(df.isnull().sum().sum()))  # pragma: no cover

    console.print(table)  # pragma: no cover

    # Create a table for column details
    col_table = Table(title="Column Details", show_header=True, header_style="bold cyan", expand=True)  # pragma: no cover
    col_table.add_column("Column Name", style="bold")  # pragma: no cover
    col_table.add_column("Type")  # pragma: no cover
    col_table.add_column("Unique Values")  # pragma: no cover
    col_table.add_column("Example (First Row)")  # pragma: no cover

    for col in df.columns:  # pragma: no cover
        example = str(df[col].iloc[0]) if not df.empty else "N/A"  # pragma: no cover
        col_table.add_row(  # pragma: no cover
            col,
            str(df[col].dtype),
            str(df[col].nunique()),
            example
        )

    console.print(col_table)  # pragma: no cover

    # Show head
    head_table = Table(title="First 5 Rows", show_header=True, header_style="bold green", expand=True)  # pragma: no cover
    for col in df.columns:  # pragma: no cover
        head_table.add_column(col)  # pragma: no cover

    for i in range(min(5, len(df))):  # pragma: no cover
        row = [str(x) for x in df.iloc[i]]  # pragma: no cover
        head_table.add_row(*row)  # pragma: no cover

    console.print(head_table)  # pragma: no cover

def export_report(history):
    """Exports the conversation history to a markdown file."""
    filename = "analysis_report.md"  # pragma: no cover
    with open(filename, "w") as f:  # pragma: no cover
        f.write("# Data Analysis Report\n\n")  # pragma: no cover
        for q, a in history:  # pragma: no cover
            f.write(f"## Question: {q}\n\n")  # pragma: no cover
            f.write(f"**Answer:**\n{a}\n\n")  # pragma: no cover
            f.write("---\n\n")  # pragma: no cover
    console.print(f"[bold green]Report exported to {filename}[/bold green]")  # pragma: no cover

def main():
    console.print(Panel.fit(
        "[bold cyan]AI Data Analyst[/bold cyan]\n[dim]Analyze CSV/Excel files with natural language[/dim]",
        border_style="blue"
    ))

    # Ask for file path, default to data.csv if exists
    default_file = "data.csv" if os.path.exists("data.csv") else "apps/agents/data-analyst/data.csv"
    if not os.path.exists(default_file):
        default_file = "" # Prompt for it if default not found  # pragma: no cover

    filepath = Prompt.ask("Enter path to CSV/Excel file", default=default_file)

    if not os.path.exists(filepath):
        console.print(f"[bold red]File not found:[/bold red] {filepath}")
        return

    with Progress(  # pragma: no cover
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Loading data...", total=None)  # pragma: no cover
        df = load_data(filepath)  # pragma: no cover

    if df is None:  # pragma: no cover
        return  # pragma: no cover

    show_summary(df)  # pragma: no cover

    # Initialize Agent
    console.print(Panel("Initializing AI Agent...", style="yellow"))  # pragma: no cover
    try:  # pragma: no cover
        agent = create_agent(df)  # pragma: no cover
    except Exception as e:  # pragma: no cover
         console.print(f"[bold red]Error initializing agent:[/bold red] {e}")  # pragma: no cover
         return  # pragma: no cover

    console.print("[bold green]Agent ready! Ask questions about your data. Type 'exit' to quit or 'export' to save report.[/bold green]")  # pragma: no cover

    history = []  # pragma: no cover

    while True:  # pragma: no cover
        user_input = Prompt.ask("\n[bold cyan]Query[/bold cyan]")  # pragma: no cover

        if user_input.lower() in ['exit', 'quit']:  # pragma: no cover
            break  # pragma: no cover

        if user_input.lower() == 'export':  # pragma: no cover
            export_report(history)  # pragma: no cover
            continue  # pragma: no cover

        if not user_input.strip():  # pragma: no cover
            continue  # pragma: no cover

        with Progress(  # pragma: no cover
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Analyzing...", total=None)  # pragma: no cover
            try:  # pragma: no cover
                # AgentExecutor invoke method
                result = agent.invoke({"input": user_input})  # pragma: no cover
                response = result.get("output", str(result))  # pragma: no cover
            except Exception as e:  # pragma: no cover
                response = f"Error: {str(e)}"  # pragma: no cover

        console.print(Panel(Markdown(response), title="AI Response", border_style="green"))  # pragma: no cover
        history.append((user_input, response))  # pragma: no cover

    console.print("[bold blue]Goodbye![/bold blue]")  # pragma: no cover

if __name__ == "__main__":
    main()
