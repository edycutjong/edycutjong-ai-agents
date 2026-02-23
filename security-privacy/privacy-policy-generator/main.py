import argparse
import sys
from pathlib import Path
from typing import Dict, Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich import print as rprint

# Import from local modules
from agent.scanner import CodeScanner
from agent.generator import PolicyGenerator
from agent.formatter import PolicyFormatter
from config import Config
from prompts.templates import POLICY_USER_PROMPT

def run_scan(directory: str, console: Console) -> Dict[str, Any]:
    """Scans the directory and displays results."""
    console.print(f"[bold blue]Scanning directory:[/bold blue] {directory}")

    scanner = CodeScanner(directory)
    try:
        results = scanner.scan()
    except Exception as e:
        console.print(f"[bold red]Error during scan:[/bold red] {e}")
        return {}

    console.print(f"[green]Scan complete![/green] Scanned {results.get('files_scanned', 0)} files.")

    # PII Table
    pii_table = Table(title="Detected PII (Personally Identifiable Information)")
    pii_table.add_column("Category", style="cyan")
    pii_table.add_column("Occurrences", style="magenta")

    pii_data = results.get("pii", [])
    if pii_data:
        for item in pii_data:
            files = results.get("details", {}).get(item, [])
            count = len(files)
            file_list = ", ".join(files[:3]) + ("..." if count > 3 else "")
            pii_table.add_row(item, f"{count} files ({file_list})")
    else:
        pii_table.add_row("None", "-")

    console.print(pii_table)

    # Third Party Table
    tp_table = Table(title="Detected Third-Party Services")
    tp_table.add_column("Service", style="green")
    tp_table.add_column("Occurrences", style="magenta")

    tp_data = results.get("third_parties", [])
    if tp_data:
        for item in tp_data:
            files = results.get("details", {}).get(item, [])
            count = len(files)
            file_list = ", ".join(files[:3]) + ("..." if count > 3 else "")
            tp_table.add_row(item, f"{count} files ({file_list})")
    else:
        tp_table.add_row("None", "-")

    console.print(tp_table)

    return results

def run_generate(directory: str, policy_type: str, output: str, console: Console):
    """Scans and generates a policy."""
    results = run_scan(directory, console)
    if not results:
        return

    console.print(f"\n[bold blue]Generating {policy_type.upper()} Policy...[/bold blue]")

    # Check for API Key
    if not Config.OPENAI_API_KEY:
        console.print("[bold red]Error:[/bold red] OPENAI_API_KEY not found in environment variables. Cannot generate policy.")
        return

    generator = PolicyGenerator(model_name=Config.MODEL_NAME, api_key=Config.OPENAI_API_KEY)

    # Using generic placeholders for CLI, ideally would ask user input
    app_name = Path(directory).name
    company_name = "Your Company Name"
    contact_email = "privacy@example.com"

    # Override the user prompt in generator (currently generator.py has hardcoded prompt construction inside)
    # Ideally, we should update generator.py to accept custom prompts or context.
    # Let's check generator.py implementation.
    # It constructs prompt inside `generate_policy`.
    # It takes scan_results and policy_type.
    # It doesn't use the templates from prompts/templates.py yet.
    # I should update generator.py to use the templates.

    context = {
        "app_name": app_name,
        "company_name": company_name,
        "contact_email": contact_email
    }

    policy_content = generator.generate_policy(results, policy_type, **context)

    output_path = Path(output)
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    md_file = output_path / f"privacy_policy_{policy_type}.md"
    html_file = output_path / f"privacy_policy_{policy_type}.html"

    md_file.write_text(policy_content)
    console.print(f"[green]Markdown policy saved to:[/green] {md_file}")

    html_content = PolicyFormatter.to_html(policy_content, title=f"{app_name} Privacy Policy")
    html_file.write_text(html_content)
    console.print(f"[green]HTML policy saved to:[/green] {html_file}")


def main():
    parser = argparse.ArgumentParser(description="Privacy Policy Generator Agent")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Scan Command
    scan_parser = subparsers.add_parser("scan", help="Scan a directory for PII and third-party services")
    scan_parser.add_argument("directory", help="Path to the codebase directory")

    # Generate Command
    gen_parser = subparsers.add_parser("generate", help="Generate a privacy policy")
    gen_parser.add_argument("directory", help="Path to the codebase directory")
    gen_parser.add_argument("--type", choices=["gdpr", "ccpa", "generic"], default="gdpr", help="Type of policy to generate")
    gen_parser.add_argument("--output", default="output", help="Output directory")

    args = parser.parse_args()
    console = Console()

    if args.command == "scan":
        run_scan(args.directory, console)
    elif args.command == "generate":
        run_generate(args.directory, args.type, args.output, console)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
