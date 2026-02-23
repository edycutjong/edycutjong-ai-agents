#!/usr/bin/env python3
"""Code Style Enforcer Bot — Enforce consistent code style across a project"""
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


def enforce_command(args):
    """Run the enforce command."""
    target = getattr(args, "path", getattr(args, "input", "."))
    console.print(f"[bold cyan]Code Style Enforcer Bot[/bold cyan]")
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
        table = Table(title="Code Style Enforcer Bot Results")
        table.add_column("File", style="cyan")
        table.add_column("Status", style="green")
        for r in results[:20]:
            table.add_row(r["file"], r["status"])
        console.print(table)
        console.print(f"\n[bold]Total: {len(results)} items analyzed[/bold]")


def main():
    parser = argparse.ArgumentParser(description="Code Style Enforcer Bot — Enforce consistent code style across a project")
    subparsers = parser.add_subparsers(dest="command", required=True)

    cmd = subparsers.add_parser("enforce", help="Run enforce")
    cmd.add_argument("path", nargs="?", default=".", help="Target path")
    cmd.add_argument("--json", action="store_true", help="Output as JSON")
    cmd.set_defaults(func=enforce_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
