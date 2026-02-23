import sys
import argparse
import os
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.syntax import Syntax

# Add current directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.parser import FigmaParser
from agent.generator import CSSGenerator
from agent.agent import FigmaAgent
from config import OPENAI_API_KEY

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Figma to CSS Agent")
    parser.add_argument("--file", "-f", help="Path to Figma JSON file")
    parser.add_argument("--mode", "-m", choices=["direct", "agent"], default="direct", help="Mode of operation")
    parser.add_argument("--format", choices=["css", "scss", "css-in-js"], default="css", help="Output format for direct mode")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive agent session")

    args = parser.parse_args()

    console.print(Panel.fit("[bold blue]Figma to CSS Agent[/bold blue]", subtitle="Convert designs to code"))

    if args.interactive:
        run_interactive_agent()
    elif args.file:
        if args.mode == "direct":
            run_direct_conversion(args.file, args.format)
        else:
            run_agent_on_file(args.file)
    else:
        # Default to interactive if no args provided
        console.print("[yellow]No arguments provided. Starting interactive mode...[/yellow]")
        run_interactive_agent()

def run_direct_conversion(filepath: str, format: str):
    """Runs direct conversion without LLM."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        console.print(f"[green]Parsing {filepath}...[/green]")
        parser = FigmaParser(data)
        nodes = parser.parse()

        console.print(f"[green]Generating {format.upper()}...[/green]")
        generator = CSSGenerator(nodes)

        if format == "scss":
            output = generator.generate_scss()
            lexer = "scss"
        elif format == "css-in-js":
            output = generator.generate_css_in_js()
            lexer = "javascript"
        else:
            output = generator.generate_css()
            lexer = "css"

        console.print(Panel(Syntax(output, lexer, theme="monokai"), title="Generated Code"))

        # Option to save
        save = Prompt.ask("Save to file?", choices=["y", "n"], default="n")
        if save == "y":
            out_path = Prompt.ask("Enter filename", default=f"output.{format if format != 'css-in-js' else 'js'}")
            with open(out_path, 'w') as f:
                f.write(output)
            console.print(f"[bold green]Saved to {out_path}[/bold green]")

    except FileNotFoundError:
        console.print(f"[red]Error: File {filepath} not found.[/red]")
    except json.JSONDecodeError:
        console.print(f"[red]Error: Invalid JSON in {filepath}.[/red]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

def run_agent_on_file(filepath: str):
    """Runs the agent with the file content as context."""
    if not OPENAI_API_KEY:
        console.print("[red]Error: OPENAI_API_KEY is missing. Cannot use agent mode.[/red]")
        return

    try:
        with open(filepath, 'r') as f:
            content = f.read()

        # Check if file is too large for context window, maybe truncate or warn
        if len(content) > 100000:
             console.print("[yellow]Warning: File is very large. Agent might struggle with context limits.[/yellow]")

        agent = FigmaAgent()
        prompt = f"Here is the Figma JSON content: {content[:20000]}... (truncated if too long). Please analyze this and generate CSS."

        console.print("[green]Agent is thinking...[/green]")
        response = agent.run(prompt)
        console.print(Panel(response, title="Agent Response"))

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

def run_interactive_agent():
    """Starts a chat session with the agent."""
    if not OPENAI_API_KEY:
        console.print("[red]Error: OPENAI_API_KEY is missing. Cannot use agent mode.[/red]")
        return

    agent = FigmaAgent()
    console.print("[bold]Interactive Agent Mode[/bold]. Type 'exit' to quit.")

    while True:
        user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
        if user_input.lower() in ["exit", "quit"]:
            break

        with console.status("Agent is working...", spinner="dots"):
            response = agent.run(user_input)

        console.print(Panel(response, title="Agent"))

if __name__ == "__main__":
    main()
