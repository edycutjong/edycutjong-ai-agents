import argparse
import os
import sys

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.scanner import Scanner
from agent.generator import AltTextGenerator
from agent.reporter import Reporter
from agent.utils import get_image_data
from config import config

# Import rich components inside main or global if installed
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import track
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Warning: 'rich' library not installed. Falling back to simple output.")

def main():
    parser = argparse.ArgumentParser(description="Image Alt Text Writer")
    parser.add_argument("path", help="Path to HTML file or directory")
    parser.add_argument("--recursive", "-r", action="store_true", help="Recursively scan directory")
    parser.add_argument("--output-format", "-f", choices=["json", "markdown"], default=config.OUTPUT_FORMAT, help="Output format for report")
    parser.add_argument("--provider", choices=["openai", "google"], default=config.DEFAULT_PROVIDER, help="LLM Provider")

    args = parser.parse_args()

    if RICH_AVAILABLE:
        console = Console()
        print_func = console.print
    else:
        print_func = print

    # Validate keys
    try:
        if args.provider == "openai" and not config.OPENAI_API_KEY:
             if RICH_AVAILABLE:
                 console.print("[bold yellow]Warning:[/bold yellow] OPENAI_API_KEY not set. AI generation might fail.")
             else:
                 print("Warning: OPENAI_API_KEY not set. AI generation might fail.")
        if args.provider == "google" and not config.GEMINI_API_KEY:
             if RICH_AVAILABLE:
                 console.print("[bold yellow]Warning:[/bold yellow] GEMINI_API_KEY not set. AI generation might fail.")
             else:
                 print("Warning: GEMINI_API_KEY not set. AI generation might fail.")
    except Exception:
        pass

    if RICH_AVAILABLE:
        console.print("[bold blue]Image Alt Text Writer[/bold blue]")

    # Initialize components
    scanner = Scanner()
    try:
        generator = AltTextGenerator(provider=args.provider)
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[bold red]Error initializing AI Generator:[/bold red] {e}")
        else:
            print(f"Error initializing AI Generator: {e}")
        return

    reporter = Reporter(output_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports"))

    # Scan for images
    if RICH_AVAILABLE:
        console.print(f"Scanning [green]{args.path}[/green]...")
    else:
        print(f"Scanning {args.path}...")

    if os.path.isfile(args.path):
        images = scanner.scan_file(args.path)
    elif os.path.isdir(args.path):
        images = scanner.scan_directory(args.path, recursive=args.recursive)
    else:
        if RICH_AVAILABLE:
            console.print(f"[bold red]Invalid path:[/bold red] {args.path}")
        else:
            print(f"Invalid path: {args.path}")
        return

    if RICH_AVAILABLE:
        console.print(f"Found [bold yellow]{len(images)}[/bold yellow] images missing alt text.")
    else:
        print(f"Found {len(images)} images missing alt text.")

    results = []

    # Process images
    if images:
        iterator = track(images, description="Processing images...") if RICH_AVAILABLE else images

        for i, img in enumerate(iterator):
            if not RICH_AVAILABLE:
                 print(f"Processing image {i+1}/{len(images)}: {img.src}")

            # Resolve base path for local images
            base_path = os.path.dirname(img.filepath)

            image_data = get_image_data(img.src, base_path=base_path)

            if image_data:
                alt_text = generator.generate_alt_text(image_data, context=img.context)
                if not RICH_AVAILABLE:
                    print(f"  Generated Alt: {alt_text}")

                result = img.to_dict()
                result["suggested_alt"] = alt_text
                results.append(result)
            else:
                if not RICH_AVAILABLE:
                    print(f"  Skipping image (could not load): {img.src}")
                result = img.to_dict()
                result["error"] = "Could not load image"
                results.append(result)

    # Generate report
    if results:
        report_path = reporter.generate_report(results, format=args.output_format)
        if RICH_AVAILABLE:
            console.print(f"[bold green]Report generated at:[/bold green] {report_path}")

            # Show summary table
            table = Table(title="Generated Alt Text Summary")
            table.add_column("Source", style="cyan", no_wrap=True)
            table.add_column("Suggested Alt Text", style="magenta")

            for res in results[:5]:  # Show first 5
                 src = res.get("src", "")
                 alt = res.get("suggested_alt", res.get("error", "N/A"))
                 table.add_row(src[:30] + "..." if len(src) > 30 else src, alt)

            if len(results) > 5:
                table.add_row("...", "...")

            console.print(table)
        else:
            print(f"Report generated at: {report_path}")

    else:
        if RICH_AVAILABLE:
            console.print("No results to report.")
        else:
            print("No results to report.")

if __name__ == "__main__":
    main()
