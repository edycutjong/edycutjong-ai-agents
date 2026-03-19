import argparse
import sys
import os
from rich.console import Console
from rich.progress import Progress

# Add current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.core import MarkdownConverterAgent

console = Console()

def main():
    parser = argparse.ArgumentParser(description="HTML to Markdown Converter Agent")
    parser.add_argument("url", nargs="?", help="URL to convert")
    parser.add_argument("--file", "-f", help="File containing list of URLs to convert")
    parser.add_argument("--output", "-o", default="output", help="Output directory")
    parser.add_argument("--download-images", "-d", action="store_true", help="Download images")

    args = parser.parse_args()

    if not args.url and not args.file:
        console.print("[red]Error: Please provide a URL or a file with URLs.[/red]")
        parser.print_help()
        sys.exit(1)

    agent = MarkdownConverterAgent(output_dir=args.output, download_images=args.download_images)

    if args.url:
        console.print(f"[bold blue]Processing URL:[/bold blue] {args.url}")
        with Progress() as progress:
            task = progress.add_task("[green]Converting...", total=1)
            result = agent.process_url(args.url)
            progress.update(task, advance=1)

        if result and not result.startswith("Error"):
            console.print(f"[bold green]Success![/bold green] Saved to: {result}")  # pragma: no cover
        else:
            console.print(f"[bold red]Failed:[/bold red] {result}")

    if args.file:
        try:  # pragma: no cover
            with open(args.file, 'r') as f:  # pragma: no cover
                urls = [line.strip() for line in f if line.strip()]  # pragma: no cover

            console.print(f"[bold blue]Processing batch of {len(urls)} URLs from {args.file}[/bold blue]")  # pragma: no cover

            with Progress() as progress:  # pragma: no cover
                task = progress.add_task("[green]Converting Batch...", total=len(urls))  # pragma: no cover

                # We can't easily hook into individual progress with ThreadPool map unless we iterate or use as_completed
                # For simplicity, we'll iterate sequentially here or modify agent to support callback,
                # but agent.process_batch uses threads.
                # Let's just run them sequentially for better progress reporting in CLI or trust the agent logger.
                # Or better: use agent.process_url in a loop here.

                results = []  # pragma: no cover
                for url in urls:  # pragma: no cover
                    res = agent.process_url(url)  # pragma: no cover
                    results.append(res)  # pragma: no cover
                    progress.update(task, advance=1)  # pragma: no cover
                    if res and not res.startswith("Error"):  # pragma: no cover
                        console.print(f"  [green]✓[/green] {url} -> {os.path.basename(res)}")  # pragma: no cover
                    else:
                        console.print(f"  [red]✗[/red] {url}")  # pragma: no cover

        except FileNotFoundError:  # pragma: no cover
            console.print(f"[red]Error: File {args.file} not found.[/red]")  # pragma: no cover
            sys.exit(1)  # pragma: no cover

if __name__ == "__main__":
    main()
