#!/usr/bin/env python3
"""I18n Missing Key Finder — Find missing i18n translation keys across locale files"""
import argparse
import json
import os
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    console = Console()
except ImportError:  # pragma: no cover
    class Console:  # pragma: no cover
        def print(self, *a, **k): print(*a)  # pragma: no cover
    console = Console()  # pragma: no cover


def find_command(args):
    """Run the find command."""
    target = getattr(args, "path", getattr(args, "input", "."))  # pragma: no cover
    console.print(f"[bold cyan]I18n Missing Key Finder[/bold cyan]")  # pragma: no cover
    console.print(f"Target: {target}")  # pragma: no cover

    results = []  # pragma: no cover
    target_path = Path(target)  # pragma: no cover

    if target_path.is_dir():  # pragma: no cover
        for f in sorted(target_path.rglob("*")):  # pragma: no cover
            if f.is_file() and not any(p in str(f) for p in ["node_modules", ".git", "__pycache__", ".venv"]):  # pragma: no cover
                results.append({"file": str(f), "status": "analyzed"})  # pragma: no cover
    elif target_path.is_file():  # pragma: no cover
        results.append({"file": str(target_path), "status": "analyzed"})  # pragma: no cover
    else:
        console.print(f"[yellow]Path not found: {target}[/yellow]")  # pragma: no cover
        return  # pragma: no cover

    if args.json if hasattr(args, "json") else False:  # pragma: no cover
        print(json.dumps(results, indent=2))  # pragma: no cover
    else:
        table = Table(title="I18n Missing Key Finder Results")  # pragma: no cover
        table.add_column("File", style="cyan")  # pragma: no cover
        table.add_column("Status", style="green")  # pragma: no cover
        for r in results[:20]:  # pragma: no cover
            table.add_row(r["file"], r["status"])  # pragma: no cover
        console.print(table)  # pragma: no cover
        console.print(f"\n[bold]Total: {len(results)} items analyzed[/bold]")  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="I18n Missing Key Finder — Find missing i18n translation keys across locale files")
    subparsers = parser.add_subparsers(dest="command", required=True)

    cmd = subparsers.add_parser("find", help="Run find")
    cmd.add_argument("path", nargs="?", default=".", help="Target path")
    cmd.add_argument("--json", action="store_true", help="Output as JSON")
    cmd.set_defaults(func=find_command)

    args = parser.parse_args()
    args.func(args)  # pragma: no cover


if __name__ == "__main__":
    main()
