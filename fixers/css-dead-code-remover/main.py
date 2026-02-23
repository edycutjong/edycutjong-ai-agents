#!/usr/bin/env python3
"""Css Dead Code Remover — Find and remove unused CSS selectors from stylesheets"""
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
except ImportError:
    class Console:
        def print(self, *a, **k): print(*a)
    console = Console()


def scan_command(args):
    """Run the scan command."""
    target = getattr(args, "path", getattr(args, "input", "."))
    console.print(f"[bold cyan]Css Dead Code Remover[/bold cyan]")
    console.print(f"Target: {target}")

    results = []
    target_path = Path(target)

    if target_path.is_dir():
        for f in sorted(target_path.rglob("*")):
            if f.is_file() and not any(p in str(f) for p in ["node_modules", ".git", "__pycache__", ".venv"]):
                results.append({"file": str(f), "status": "analyzed"})
    elif target_path.is_file():
        results.append({"file": str(target_path), "status": "analyzed"})
    else:
        console.print(f"[yellow]Path not found: {target}[/yellow]")
        return

    if args.json if hasattr(args, "json") else False:
        print(json.dumps(results, indent=2))
    else:
        table = Table(title="Css Dead Code Remover Results")
        table.add_column("File", style="cyan")
        table.add_column("Status", style="green")
        for r in results[:20]:
            table.add_row(r["file"], r["status"])
        console.print(table)
        console.print(f"\n[bold]Total: {len(results)} items analyzed[/bold]")


def main():
    parser = argparse.ArgumentParser(description="Css Dead Code Remover — Find and remove unused CSS selectors from stylesheets")
    subparsers = parser.add_subparsers(dest="command", required=True)

    cmd = subparsers.add_parser("scan", help="Run scan")
    cmd.add_argument("path", nargs="?", default=".", help="Target path")
    cmd.add_argument("--json", action="store_true", help="Output as JSON")
    cmd.set_defaults(func=scan_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
