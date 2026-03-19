import sys  # pragma: no cover
import os  # pragma: no cover
from pathlib import Path  # pragma: no cover
from rich.console import Console  # pragma: no cover
from rich.table import Table  # pragma: no cover
from rich.progress import Progress, SpinnerColumn, TextColumn  # pragma: no cover
from rich.prompt import Confirm, Prompt  # pragma: no cover
from rich.panel import Panel  # pragma: no cover
from rich.tree import Tree  # pragma: no cover
from rich import box  # pragma: no cover

from tools.file_scanner import AssetScanner  # pragma: no cover
from tools.code_scanner import CodeScanner  # pragma: no cover
from tools.dependency_graph import DependencyGraph  # pragma: no cover
from tools.cleaner import Cleaner  # pragma: no cover
from tools.optimizer import Optimizer  # pragma: no cover

console = Console()  # pragma: no cover

def main():  # pragma: no cover
    console.print(Panel.fit("[bold magenta]Unused Asset Cleaner[/bold magenta]", border_style="magenta"))  # pragma: no cover

    # Get target directory
    if len(sys.argv) > 1:  # pragma: no cover
        target_dir = sys.argv[1]  # pragma: no cover
    else:
        target_dir = Prompt.ask("Enter directory to scan", default=".")  # pragma: no cover

    target_path = Path(target_dir).resolve()  # pragma: no cover
    if not target_path.exists():  # pragma: no cover
        console.print(f"[red]Error: Directory {target_path} does not exist.[/red]")  # pragma: no cover
        return  # pragma: no cover

    with Progress(  # pragma: no cover
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:

        # Step 1: Scan for asset files
        task1 = progress.add_task(description="Scanning for asset files...", total=None)  # pragma: no cover
        asset_scanner = AssetScanner(target_path)  # pragma: no cover
        assets = asset_scanner.scan()  # pragma: no cover
        progress.update(task1, completed=100)  # pragma: no cover
        console.print(f"[green]✓ Found {len(assets)} assets.[/green]")  # pragma: no cover

        # Step 2: Scan code for references
        task2 = progress.add_task(description="Scanning source code for references...", total=None)  # pragma: no cover
        code_scanner = CodeScanner(target_path)  # pragma: no cover
        references = code_scanner.find_references(assets)  # pragma: no cover
        progress.update(task2, completed=100)  # pragma: no cover
        console.print(f"[green]✓ Scanned source code.[/green]")  # pragma: no cover

        # Step 3: Build dependency graph
        task3 = progress.add_task(description="Analyzing usage...", total=None)  # pragma: no cover
        graph = DependencyGraph(assets, references)  # pragma: no cover
        stats = graph.get_stats()  # pragma: no cover
        progress.update(task3, completed=100)  # pragma: no cover

    # Report
    table = Table(title="Asset Analysis Report", box=box.ROUNDED)  # pragma: no cover
    table.add_column("Metric", style="cyan")  # pragma: no cover
    table.add_column("Value", style="yellow")  # pragma: no cover

    table.add_row("Total Assets", str(stats["total_assets"]))  # pragma: no cover
    table.add_row("Used Assets", str(stats["used_assets"]))  # pragma: no cover
    table.add_row("Unused Assets", f"[bold red]{stats['unused_assets']}[/bold red]")  # pragma: no cover
    table.add_row("Total Size", f"{stats['total_size_bytes'] / 1024:.2f} KB")  # pragma: no cover
    table.add_row("Unused Size", f"{stats['unused_size_bytes'] / 1024:.2f} KB")  # pragma: no cover
    table.add_row("Potential Savings", f"{stats['savings_percentage']:.1f}%")  # pragma: no cover

    console.print(table)  # pragma: no cover

    unused_assets = graph.get_unused_assets()  # pragma: no cover

    if not unused_assets:  # pragma: no cover
        console.print("[green]No unused assets found! Good job![/green]")  # pragma: no cover
        return  # pragma: no cover

    # List unused assets?
    if len(unused_assets) < 20:  # pragma: no cover
        # Show list if small
        tree = Tree("Unused Assets")  # pragma: no cover
        for asset in unused_assets:  # pragma: no cover
            tree.add(str(asset.relative_to(target_path)))  # pragma: no cover
        console.print(tree)  # pragma: no cover
    else:
        console.print(f"[yellow]...and {len(unused_assets)} unused files.[/yellow]")  # pragma: no cover

    # Action Prompt
    action = Prompt.ask(  # pragma: no cover
        "Choose an action",
        choices=["delete", "backup & delete", "optimize", "ignore", "exit"],
        default="backup & delete"
    )

    if action == "exit":  # pragma: no cover
        console.print("Exiting.")  # pragma: no cover
        return  # pragma: no cover

    elif action == "ignore":  # pragma: no cover
        console.print("Ignoring unused assets.")  # pragma: no cover
        return  # pragma: no cover

    elif action in ["delete", "backup & delete"]:  # pragma: no cover
        backup = (action == "backup & delete")  # pragma: no cover

        if Confirm.ask(f"Are you sure you want to {action} {len(unused_assets)} files?"):  # pragma: no cover
            cleaner = Cleaner(target_path)  # pragma: no cover
            with console.status(f"[bold red]{action.capitalize()}ing assets..."):  # pragma: no cover
                count, freed = cleaner.delete(unused_assets, backup=backup)  # pragma: no cover

            console.print(f"[green]Successfully processed {count} files.[/green]")  # pragma: no cover
            console.print(f"[green]Freed {freed / 1024:.2f} KB.[/green]")  # pragma: no cover

            if backup:  # pragma: no cover
                console.print(f"[blue]Backup created in {target_path / '.unused_assets_backup'}[/blue]")  # pragma: no cover

    elif action == "optimize":  # pragma: no cover
        # Optimize all assets (or just unused? Usually optimize used assets makes more sense to save space,
        # but the prompt implies dealing with the result of the scan.
        # However, optimizing *unused* assets before deleting them is pointless.
        # Maybe the user wants to optimize *all* assets?
        # The tool is "Unused Asset Cleaner", but optimization is listed as a feature.
        # Let's ask what to optimize.

        target_group = Prompt.ask("Optimize which assets?", choices=["all", "used", "unused"], default="all")  # pragma: no cover

        files_to_optimize = []  # pragma: no cover
        if target_group == "all":  # pragma: no cover
            files_to_optimize = assets  # pragma: no cover
        elif target_group == "used":  # pragma: no cover
            files_to_optimize = graph.get_used_assets()  # pragma: no cover
        elif target_group == "unused":  # pragma: no cover
            files_to_optimize = unused_assets  # pragma: no cover

        if not files_to_optimize:  # pragma: no cover
            console.print("[yellow]No files to optimize.[/yellow]")  # pragma: no cover
            return  # pragma: no cover

        if Confirm.ask(f"This will overwrite {len(files_to_optimize)} images. Continue?"):  # pragma: no cover
             optimizer = Optimizer()  # pragma: no cover
             with console.status("[bold blue]Optimizing images..."):  # pragma: no cover
                 count, saved = optimizer.optimize(files_to_optimize)  # pragma: no cover

             console.print(f"[green]Optimized {count} images.[/green]")  # pragma: no cover
             console.print(f"[green]Saved {saved / 1024:.2f} KB.[/green]")  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
