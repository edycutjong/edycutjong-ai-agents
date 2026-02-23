import os
import argparse
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.markdown import Markdown

from tools.git_ops import GitHandler, PRHandler
from tools.analyzer import CodeAnalyzer
from tools.doc_manager import DocManager
from tools.generator import DocGenerator

# Load environment variables
load_dotenv()

console = Console()

def print_banner():
    banner = """
    [bold magenta]Doc Drift Fixer[/bold magenta]
    [cyan]Aligning Code and Documentation with Precision[/cyan]
    """
    console.print(Panel(banner, border_style="magenta"))

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Fix documentation drift based on code changes.")
    parser.add_argument("--repo-path", default=".", help="Path to the repository (default: current directory)")
    parser.add_argument("--target-branch", default="main", help="Target branch to compare against (default: main)")
    parser.add_argument("--pr", type=int, help="PR number to analyze (requires GITHUB_TOKEN)")
    parser.add_argument("--dry-run", action="store_true", help="Don't apply changes, just show proposals")

    args = parser.parse_args()

    repo_path = args.repo_path
    target_branch = args.target_branch
    pr_number = args.pr
    dry_run = args.dry_run

    openai_key = os.getenv("OPENAI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    if not openai_key:
        console.print("[yellow]Warning: OPENAI_API_KEY not found. AI generation will be disabled.[/yellow]")

    # Initialize Tools
    try:
        git_handler = GitHandler(repo_path)
        code_analyzer = CodeAnalyzer()
        doc_manager = DocManager(repo_path)
        doc_generator = DocGenerator(openai_key)
    except Exception as e:
        console.print(f"[bold red]Error initializing tools:[/bold red] {e}")
        sys.exit(1)

    # 1. Get Changes
    changes = []
    diff_content = ""

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Analyzing repository...", total=None)

        if pr_number:
            if not github_token:
                console.print("[bold red]Error: GITHUB_TOKEN required for PR analysis.[/bold red]")
                sys.exit(1)

            # Try to get repo name from origin
            repo_name = "unknown/unknown"
            try:
                remote_url = git_handler.repo.remotes.origin.url
                if "github.com" in remote_url:
                    parts = remote_url.split("github.com")[-1].replace(":", "/").strip("/").replace(".git", "")
                    repo_name = parts
            except:
                pass

            pr_handler = PRHandler(repo_name, pr_number, github_token)
            progress.update(task, description=f"Fetching PR #{pr_number}...")

            changes = pr_handler.get_changed_files()
            changes = [f for f in changes if f.endswith(".py")]
        else:
            progress.update(task, description=f"Comparing with {target_branch}...")
            changes = git_handler.list_changed_files(target_branch)
            # Filter for source code files (py, js, ts, etc)
            # For now, just Python
            changes = [f for f in changes if f.endswith(".py")]

    if not changes:
        console.print("[green]No code changes detected.[/green]")
        return

    console.print(f"[bold cyan]Detected {len(changes)} changed files:[/bold cyan]")
    for f in changes:
        console.print(f" - {f}")

    # 2. Process each changed file
    for file_path in changes:
        full_path = os.path.join(repo_path, file_path)
        # Skip existence check for PR unless we want to ensure local sync
        if not pr_number and not os.path.exists(full_path):
             continue # File deleted locally

        console.print(Panel(f"[bold]Processing {file_path}[/bold]", style="blue"))

        # Display Code Structure Summary
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r') as f:
                    code_content = f.read()
                structure = code_analyzer.analyze_code(code_content)
                if "definitions" in structure and structure["definitions"]:
                    console.print("[dim]Detected definitions:[/dim]")
                    for d in structure["definitions"]:
                        console.print(f"  - [dim]{d['type']}: {d['name']}[/dim]")
            except Exception:
                pass

        # Analyze Code
        if pr_number:
             file_diff = pr_handler.get_file_patch(file_path)
        else:
             file_diff = git_handler.repo.git.diff(target_branch, file_path)

        if not file_diff:
            continue

        # Find related docs
        related_docs = doc_manager.find_related_docs(file_path)

        if not related_docs:
            console.print(f"[yellow]No related documentation found for {file_path}.[/yellow]")
            if Confirm.ask("Generate new documentation?"):
                 with open(full_path, 'r') as f:
                     code_content = f.read()
                 new_doc = doc_generator.propose_new_doc(code_content, file_path)
                 console.print(Markdown(new_doc))
                 if not dry_run and Confirm.ask("Save this new documentation?"):
                     new_doc_path = Prompt.ask("Enter path for new doc", default=f"docs/{os.path.basename(file_path).replace('.py', '.md')}")
                     os.makedirs(os.path.dirname(new_doc_path), exist_ok=True)
                     with open(new_doc_path, 'w') as f:
                         f.write(new_doc)
                     console.print(f"[green]Saved to {new_doc_path}[/green]")
        else:
            for doc in related_docs:
                console.print(f"Found related doc: [underline]{doc}[/underline]")
                with open(doc, 'r') as f:
                    current_doc = f.read()

                # Check links first
                broken_links = doc_manager.check_links(doc)
                if broken_links:
                    console.print("[red]Broken links found:[/red]")
                    for link in broken_links:
                        console.print(f" - {link}")

                # Check code examples
                code_errors = doc_manager.verify_code_examples(doc)
                if code_errors:
                     console.print("[red]Code example errors found:[/red]")
                     for err in code_errors:
                         console.print(f" - {err}")

                # Generate Update
                with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as p:
                    p.add_task(description="Generating doc updates...", total=None)
                    updated_doc = doc_generator.generate_update(file_diff, current_doc)

                console.print(Panel(Markdown(updated_doc), title="Proposed Update", border_style="green"))

                if not dry_run and Confirm.ask(f"Apply update to {doc}?"):
                    # This replaces the whole doc with the 'updated section' which might be wrong
                    # if the LLM only returned a snippet.
                    # The prompt asked for "Output ONLY the updated documentation content."
                    # If it returns the full doc, we are good.
                    # If it returns a snippet, we are in trouble.
                    # Let's assume for this MVP the prompt implies rewriting the *relevant* section
                    # but since we passed the whole doc, hopefully it rewrites the whole doc or we need better chunking.
                    # For safety, let's backup
                    import shutil
                    shutil.copy(doc, doc + ".bak")
                    with open(doc, 'w') as f:
                        f.write(updated_doc) # Warning: this might overwrite with partial content if LLM fails
                    console.print(f"[green]Updated {doc} (backup at {doc}.bak)[/green]")

                    # Commit?
                    if Confirm.ask("Commit this change?"):
                        git_handler.commit_changes(f"docs: update documentation for {os.path.basename(file_path)}", [doc])
                        console.print("[green]Committed.[/green]")

if __name__ == "__main__":
    main()
