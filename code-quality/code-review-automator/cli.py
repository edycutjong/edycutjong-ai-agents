import argparse  # pragma: no cover
import sys  # pragma: no cover
import os  # pragma: no cover
from dotenv import load_dotenv  # pragma: no cover
from rich.console import Console  # pragma: no cover
from rich.table import Table  # pragma: no cover
from rich.panel import Panel  # pragma: no cover
from rich.markdown import Markdown  # pragma: no cover
from agent.github_client import GitHubClient  # pragma: no cover
from agent.reviewer import Reviewer  # pragma: no cover

load_dotenv()  # pragma: no cover
console = Console()  # pragma: no cover

def main():  # pragma: no cover
    parser = argparse.ArgumentParser(description="AI Code Review Automator CLI")  # pragma: no cover
    parser.add_argument("--repo", required=True, help="GitHub repository name (owner/repo)")  # pragma: no cover
    parser.add_argument("--pr", required=True, type=int, help="Pull Request number")  # pragma: no cover
    parser.add_argument("--token", help="GitHub Token (or set GITHUB_TOKEN env var)")  # pragma: no cover
    parser.add_argument("--api-key", help="OpenAI API Key (or set OPENAI_API_KEY env var)")  # pragma: no cover
    parser.add_argument("--post", action="store_true", help="Post comments to GitHub")  # pragma: no cover
    parser.add_argument("--focus", default="Logic,Security,Style", help="Comma-separated focus categories")  # pragma: no cover
    parser.add_argument("--guidelines", default="", help="Custom review guidelines")  # pragma: no cover

    args = parser.parse_args()  # pragma: no cover

    token = args.token or os.getenv("GITHUB_TOKEN")  # pragma: no cover
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")  # pragma: no cover

    if not token or not api_key:  # pragma: no cover
        console.print("[red]Error: GITHUB_TOKEN and OPENAI_API_KEY are required.[/red]")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    focus_list = [f.strip() for f in args.focus.split(",")]  # pragma: no cover

    try:  # pragma: no cover
        with console.status("[bold green]Fetching PR diff..."):  # pragma: no cover
            gh_client = GitHubClient(token)  # pragma: no cover
            diff_data = gh_client.get_pr_diff(args.repo, args.pr)  # pragma: no cover

        if not diff_data:  # pragma: no cover
            console.print("[yellow]No changes found in PR.[/yellow]")  # pragma: no cover
            return  # pragma: no cover

        with console.status("[bold green]Analyzing code..."):  # pragma: no cover
            reviewer = Reviewer(api_key)  # pragma: no cover
            results = reviewer.analyze_diff(diff_data, args.guidelines, focus_list)  # pragma: no cover

        summary = results.get("summary", "No summary generated.")  # pragma: no cover
        comments = results.get("comments", [])  # pragma: no cover

        console.print(Panel(Markdown(summary), title="Review Summary", border_style="blue"))  # pragma: no cover

        if comments:  # pragma: no cover
            table = Table(title="Detailed Findings")  # pragma: no cover
            table.add_column("File", style="cyan")  # pragma: no cover
            table.add_column("Line", style="magenta")  # pragma: no cover
            table.add_column("Category", style="green")  # pragma: no cover
            table.add_column("Issue", style="white")  # pragma: no cover

            for comment in comments:  # pragma: no cover
                table.add_row(  # pragma: no cover
                    comment.get('filename'),
                    str(comment.get('line')),
                    comment.get('category'),
                    comment.get('body')
                )
            console.print(table)  # pragma: no cover
        else:
            console.print("[green]No issues found![/green]")  # pragma: no cover

        if args.post:  # pragma: no cover
            with console.status("[bold blue]Posting to GitHub..."):  # pragma: no cover
                gh_client.post_general_comment(args.repo, args.pr, f"### AI Review Summary\n\n{summary}")  # pragma: no cover
                for comment in comments:  # pragma: no cover
                    try:  # pragma: no cover
                        gh_client.post_review_comment(  # pragma: no cover
                            args.repo,
                            args.pr,
                            f"**[{comment.get('category')}]** {comment.get('body')}\n\nSuggested Fix:\n```\n{comment.get('suggestion', '')}\n```",
                            comment.get('filename'),
                            int(comment.get('line'))
                        )
                    except Exception as e:  # pragma: no cover
                        console.print(f"[yellow]Failed to post comment on {comment.get('filename')}:{comment.get('line')} - {e}[/yellow]")  # pragma: no cover

            console.print("[bold green]Successfully posted review to GitHub![/bold green]")  # pragma: no cover

    except Exception as e:  # pragma: no cover
        console.print(f"[red]Error: {e}[/red]")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
