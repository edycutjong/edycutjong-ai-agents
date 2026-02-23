import sys
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.panel import Panel
from rich.tree import Tree
from rich import box

from tools.file_scanner import AssetScanner
from tools.code_scanner import CodeScanner
from tools.dependency_graph import DependencyGraph
from tools.cleaner import Cleaner
from tools.optimizer import Optimizer

console = Console()

def main():
    console.print(Panel.fit("[bold magenta]Unused Asset Cleaner[/bold magenta]", border_style="magenta"))

    # Get target directory
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = Prompt.ask("Enter directory to scan", default=".")

    target_path = Path(target_dir).resolve()
    if not target_path.exists():
        console.print(f"[red]Error: Directory {target_path} does not exist.[/red]")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:

        # Step 1: Scan for asset files
        task1 = progress.add_task(description="Scanning for asset files...", total=None)
        asset_scanner = AssetScanner(target_path)
        assets = asset_scanner.scan()
        progress.update(task1, completed=100)
        console.print(f"[green]✓ Found {len(assets)} assets.[/green]")

        # Step 2: Scan code for references
        task2 = progress.add_task(description="Scanning source code for references...", total=None)
        code_scanner = CodeScanner(target_path)
        references = code_scanner.find_references(assets)
        progress.update(task2, completed=100)
        console.print(f"[green]✓ Scanned source code.[/green]")

        # Step 3: Build dependency graph
        task3 = progress.add_task(description="Analyzing usage...", total=None)
        graph = DependencyGraph(assets, references)
        stats = graph.get_stats()
        progress.update(task3, completed=100)

    # Report
    table = Table(title="Asset Analysis Report", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="yellow")

    table.add_row("Total Assets", str(stats["total_assets"]))
    table.add_row("Used Assets", str(stats["used_assets"]))
    table.add_row("Unused Assets", f"[bold red]{stats['unused_assets']}[/bold red]")
    table.add_row("Total Size", f"{stats['total_size_bytes'] / 1024:.2f} KB")
    table.add_row("Unused Size", f"{stats['unused_size_bytes'] / 1024:.2f} KB")
    table.add_row("Potential Savings", f"{stats['savings_percentage']:.1f}%")

    console.print(table)

    unused_assets = graph.get_unused_assets()

    if not unused_assets:
        console.print("[green]No unused assets found! Good job![/green]")
        return

    # List unused assets?
    if len(unused_assets) < 20:
        # Show list if small
        tree = Tree("Unused Assets")
        for asset in unused_assets:
            tree.add(str(asset.relative_to(target_path)))
        console.print(tree)
    else:
        console.print(f"[yellow]...and {len(unused_assets)} unused files.[/yellow]")

    # Action Prompt
    action = Prompt.ask(
        "Choose an action",
        choices=["delete", "backup & delete", "optimize", "ignore", "exit"],
        default="backup & delete"
    )

    if action == "exit":
        console.print("Exiting.")
        return

    elif action == "ignore":
        console.print("Ignoring unused assets.")
        return

    elif action in ["delete", "backup & delete"]:
        backup = (action == "backup & delete")

        if Confirm.ask(f"Are you sure you want to {action} {len(unused_assets)} files?"):
            cleaner = Cleaner(target_path)
            with console.status(f"[bold red]{action.capitalize()}ing assets..."):
                count, freed = cleaner.delete(unused_assets, backup=backup)

            console.print(f"[green]Successfully processed {count} files.[/green]")
            console.print(f"[green]Freed {freed / 1024:.2f} KB.[/green]")

            if backup:
                console.print(f"[blue]Backup created in {target_path / '.unused_assets_backup'}[/blue]")

    elif action == "optimize":
        # Optimize all assets (or just unused? Usually optimize used assets makes more sense to save space,
        # but the prompt implies dealing with the result of the scan.
        # However, optimizing *unused* assets before deleting them is pointless.
        # Maybe the user wants to optimize *all* assets?
        # The tool is "Unused Asset Cleaner", but optimization is listed as a feature.
        # Let's ask what to optimize.

        target_group = Prompt.ask("Optimize which assets?", choices=["all", "used", "unused"], default="all")

        files_to_optimize = []
        if target_group == "all":
            files_to_optimize = assets
        elif target_group == "used":
            files_to_optimize = graph.get_used_assets()
        elif target_group == "unused":
            files_to_optimize = unused_assets

        if not files_to_optimize:
            console.print("[yellow]No files to optimize.[/yellow]")
            return

        if Confirm.ask(f"This will overwrite {len(files_to_optimize)} images. Continue?"):
             optimizer = Optimizer()
             with console.status("[bold blue]Optimizing images..."):
                 count, saved = optimizer.optimize(files_to_optimize)

             console.print(f"[green]Optimized {count} images.[/green]")
             console.print(f"[green]Saved {saved / 1024:.2f} KB.[/green]")

if __name__ == "__main__":
    main()
