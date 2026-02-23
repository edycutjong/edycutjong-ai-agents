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
            console.print(f"[bold green]Success![/bold green] Saved to: {result}")
        else:
            console.print(f"[bold red]Failed:[/bold red] {result}")

    if args.file:
        try:
            with open(args.file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]

            console.print(f"[bold blue]Processing batch of {len(urls)} URLs from {args.file}[/bold blue]")

            with Progress() as progress:
                task = progress.add_task("[green]Converting Batch...", total=len(urls))

                # We can't easily hook into individual progress with ThreadPool map unless we iterate or use as_completed
                # For simplicity, we'll iterate sequentially here or modify agent to support callback,
                # but agent.process_batch uses threads.
                # Let's just run them sequentially for better progress reporting in CLI or trust the agent logger.
                # Or better: use agent.process_url in a loop here.

                results = []
                for url in urls:
                    res = agent.process_url(url)
                    results.append(res)
                    progress.update(task, advance=1)
                    if res and not res.startswith("Error"):
                        console.print(f"  [green]✓[/green] {url} -> {os.path.basename(res)}")
                    else:
                        console.print(f"  [red]✗[/red] {url}")

        except FileNotFoundError:
            console.print(f"[red]Error: File {args.file} not found.[/red]")
            sys.exit(1)

if __name__ == "__main__":
    main()
