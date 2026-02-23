import argparse
import sys
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from agent.github_client import GitHubClient
from agent.reviewer import Reviewer

load_dotenv()
console = Console()

def main():
    parser = argparse.ArgumentParser(description="AI Code Review Automator CLI")
    parser.add_argument("--repo", required=True, help="GitHub repository name (owner/repo)")
    parser.add_argument("--pr", required=True, type=int, help="Pull Request number")
    parser.add_argument("--token", help="GitHub Token (or set GITHUB_TOKEN env var)")
    parser.add_argument("--api-key", help="OpenAI API Key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--post", action="store_true", help="Post comments to GitHub")
    parser.add_argument("--focus", default="Logic,Security,Style", help="Comma-separated focus categories")
    parser.add_argument("--guidelines", default="", help="Custom review guidelines")

    args = parser.parse_args()

    token = args.token or os.getenv("GITHUB_TOKEN")
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")

    if not token or not api_key:
        console.print("[red]Error: GITHUB_TOKEN and OPENAI_API_KEY are required.[/red]")
        sys.exit(1)

    focus_list = [f.strip() for f in args.focus.split(",")]

    try:
        with console.status("[bold green]Fetching PR diff..."):
            gh_client = GitHubClient(token)
            diff_data = gh_client.get_pr_diff(args.repo, args.pr)

        if not diff_data:
            console.print("[yellow]No changes found in PR.[/yellow]")
            return

        with console.status("[bold green]Analyzing code..."):
            reviewer = Reviewer(api_key)
            results = reviewer.analyze_diff(diff_data, args.guidelines, focus_list)

        summary = results.get("summary", "No summary generated.")
        comments = results.get("comments", [])

        console.print(Panel(Markdown(summary), title="Review Summary", border_style="blue"))

        if comments:
            table = Table(title="Detailed Findings")
            table.add_column("File", style="cyan")
            table.add_column("Line", style="magenta")
            table.add_column("Category", style="green")
            table.add_column("Issue", style="white")

            for comment in comments:
                table.add_row(
                    comment.get('filename'),
                    str(comment.get('line')),
                    comment.get('category'),
                    comment.get('body')
                )
            console.print(table)
        else:
            console.print("[green]No issues found![/green]")

        if args.post:
            with console.status("[bold blue]Posting to GitHub..."):
                gh_client.post_general_comment(args.repo, args.pr, f"### AI Review Summary\n\n{summary}")
                for comment in comments:
                    try:
                        gh_client.post_review_comment(
                            args.repo,
                            args.pr,
                            f"**[{comment.get('category')}]** {comment.get('body')}\n\nSuggested Fix:\n```\n{comment.get('suggestion', '')}\n```",
                            comment.get('filename'),
                            int(comment.get('line'))
                        )
                    except Exception as e:
                        console.print(f"[yellow]Failed to post comment on {comment.get('filename')}:{comment.get('line')} - {e}[/yellow]")

            console.print("[bold green]Successfully posted review to GitHub![/bold green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
