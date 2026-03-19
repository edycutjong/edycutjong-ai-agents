#!/usr/bin/env python3
"""Receipt Categorizer Agent — CLI entry point."""
import argparse
import sys
import os
import json as json_mod

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from src.agent import ReceiptCategorizerAgent
from src.utils import console, print_header, print_step, print_success, print_error


def main():
    print_header("Receipt Categorizer Agent")

    parser = argparse.ArgumentParser(description="OCR receipts and auto-categorize expenses")
    parser.add_argument("--file", "-f", help="Path to a receipt text file")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    args = parser.parse_args()

    if args.file:
        try:  # pragma: no cover
            with open(args.file, "r") as f:  # pragma: no cover
                receipt_text = f.read()  # pragma: no cover
        except FileNotFoundError:  # pragma: no cover
            print_error(f"File not found: {args.file}")  # pragma: no cover
            sys.exit(1)  # pragma: no cover
    else:
        receipt_text = Prompt.ask("[bold cyan]Paste receipt text[/bold cyan]")

    if not receipt_text.strip():
        print_error("Receipt text is empty.")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print_step("Categorizing with Gemini...")

    try:
        agent = ReceiptCategorizerAgent()
        result = agent.categorize(receipt_text)
    except Exception as e:
        print_error(f"Categorization failed: {e}")
        sys.exit(1)

    print_success("Categorization complete!")  # pragma: no cover

    # Display receipt info
    info_lines = [  # pragma: no cover
        f"[bold]Vendor:[/bold] {result.get('vendor', 'N/A')}",
        f"[bold]Date:[/bold] {result.get('date', 'Unknown')}",
        f"[bold]Category:[/bold] {result.get('category', 'Other')}",
        f"[bold]Total:[/bold] {result.get('total', 'N/A')}",
        f"[bold]Currency:[/bold] {result.get('currency', 'N/A')}",
        f"[bold]Tax:[/bold] {result.get('tax', '0.00')}",
        f"[bold]Payment:[/bold] {result.get('payment_method', 'Unknown')}",
    ]
    console.print(Panel("\n".join(info_lines), title="Receipt Summary", border_style="green"))  # pragma: no cover

    # Line items
    items = result.get("items", [])  # pragma: no cover
    if items:  # pragma: no cover
        table = Table(title="Line Items", border_style="cyan")  # pragma: no cover
        table.add_column("Item", style="bold")  # pragma: no cover
        table.add_column("Qty")  # pragma: no cover
        table.add_column("Price")  # pragma: no cover
        for item in items:  # pragma: no cover
            table.add_row(  # pragma: no cover
                item.get("name", "?"),
                str(item.get("quantity", "1")),
                str(item.get("price", "?")),
            )
        console.print(table)  # pragma: no cover

    # Summary
    summary = result.get("summary", "")  # pragma: no cover
    if summary:  # pragma: no cover
        console.print(f"\n[dim]{summary}[/dim]")  # pragma: no cover

    # Export
    if args.output:  # pragma: no cover
        try:  # pragma: no cover
            with open(args.output, "w") as f:  # pragma: no cover
                json_mod.dump(result, f, indent=2)  # pragma: no cover
            print_success(f"Saved to {args.output}")  # pragma: no cover
        except IOError as e:  # pragma: no cover
            print_error(f"Failed to save: {e}")  # pragma: no cover


if __name__ == "__main__":
    main()
