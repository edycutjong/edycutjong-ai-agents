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
        run_interactive_agent()  # pragma: no cover
    elif args.file:
        if args.mode == "direct":  # pragma: no cover
            run_direct_conversion(args.file, args.format)  # pragma: no cover
        else:
            run_agent_on_file(args.file)  # pragma: no cover
    else:
        # Default to interactive if no args provided
        console.print("[yellow]No arguments provided. Starting interactive mode...[/yellow]")
        run_interactive_agent()

def run_direct_conversion(filepath: str, format: str):
    """Runs direct conversion without LLM."""
    try:  # pragma: no cover
        with open(filepath, 'r') as f:  # pragma: no cover
            data = json.load(f)  # pragma: no cover

        console.print(f"[green]Parsing {filepath}...[/green]")  # pragma: no cover
        parser = FigmaParser(data)  # pragma: no cover
        nodes = parser.parse()  # pragma: no cover

        console.print(f"[green]Generating {format.upper()}...[/green]")  # pragma: no cover
        generator = CSSGenerator(nodes)  # pragma: no cover

        if format == "scss":  # pragma: no cover
            output = generator.generate_scss()  # pragma: no cover
            lexer = "scss"  # pragma: no cover
        elif format == "css-in-js":  # pragma: no cover
            output = generator.generate_css_in_js()  # pragma: no cover
            lexer = "javascript"  # pragma: no cover
        else:
            output = generator.generate_css()  # pragma: no cover
            lexer = "css"  # pragma: no cover

        console.print(Panel(Syntax(output, lexer, theme="monokai"), title="Generated Code"))  # pragma: no cover

        # Option to save
        save = Prompt.ask("Save to file?", choices=["y", "n"], default="n")  # pragma: no cover
        if save == "y":  # pragma: no cover
            out_path = Prompt.ask("Enter filename", default=f"output.{format if format != 'css-in-js' else 'js'}")  # pragma: no cover
            with open(out_path, 'w') as f:  # pragma: no cover
                f.write(output)  # pragma: no cover
            console.print(f"[bold green]Saved to {out_path}[/bold green]")  # pragma: no cover

    except FileNotFoundError:  # pragma: no cover
        console.print(f"[red]Error: File {filepath} not found.[/red]")  # pragma: no cover
    except json.JSONDecodeError:  # pragma: no cover
        console.print(f"[red]Error: Invalid JSON in {filepath}.[/red]")  # pragma: no cover
    except Exception as e:  # pragma: no cover
        console.print(f"[red]Error: {str(e)}[/red]")  # pragma: no cover

def run_agent_on_file(filepath: str):
    """Runs the agent with the file content as context."""
    if not OPENAI_API_KEY:  # pragma: no cover
        console.print("[red]Error: OPENAI_API_KEY is missing. Cannot use agent mode.[/red]")  # pragma: no cover
        return  # pragma: no cover

    try:  # pragma: no cover
        with open(filepath, 'r') as f:  # pragma: no cover
            content = f.read()  # pragma: no cover

        # Check if file is too large for context window, maybe truncate or warn
        if len(content) > 100000:  # pragma: no cover
             console.print("[yellow]Warning: File is very large. Agent might struggle with context limits.[/yellow]")  # pragma: no cover

        agent = FigmaAgent()  # pragma: no cover
        prompt = f"Here is the Figma JSON content: {content[:20000]}... (truncated if too long). Please analyze this and generate CSS."  # pragma: no cover

        console.print("[green]Agent is thinking...[/green]")  # pragma: no cover
        response = agent.run(prompt)  # pragma: no cover
        console.print(Panel(response, title="Agent Response"))  # pragma: no cover

    except Exception as e:  # pragma: no cover
        console.print(f"[red]Error: {str(e)}[/red]")  # pragma: no cover

def run_interactive_agent():
    """Starts a chat session with the agent."""
    if not OPENAI_API_KEY:
        console.print("[red]Error: OPENAI_API_KEY is missing. Cannot use agent mode.[/red]")  # pragma: no cover
        return  # pragma: no cover

    agent = FigmaAgent()
    console.print("[bold]Interactive Agent Mode[/bold]. Type 'exit' to quit.")

    while True:
        user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
        if user_input.lower() in ["exit", "quit"]:
            break

        with console.status("Agent is working...", spinner="dots"):  # pragma: no cover
            response = agent.run(user_input)  # pragma: no cover

        console.print(Panel(response, title="Agent"))  # pragma: no cover

if __name__ == "__main__":
    main()  # pragma: no cover
