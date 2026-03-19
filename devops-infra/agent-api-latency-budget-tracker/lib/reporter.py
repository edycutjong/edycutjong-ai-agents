from rich.console import Console
from rich.table import Table
import json
from typing import Dict, Any, List

def format_terminal(results: List[Dict[str, Any]]):
    console = Console()
    table = Table(title="API Latency Budget Report", style="cyan")
    
    table.add_column("Endpoint", style="bold white")
    table.add_column("Total Reqs", justify="right")
    table.add_column("Violations", justify="right")
    table.add_column("Budget Consumed (%)", justify="right")
    table.add_column("Status", justify="center")
    
    for res in results:
        name = res["name"]
        total = str(res["total_requests"])
        violations = str(res["violations"])
        consumed = f"{res['budget_consumed_percent']:.2f}%"
        
        status = "[green]OK[/green]"
        if res["is_exhausted"]:
            status = "[bold red]EXHAUSTED[/bold red]"
            consumed = f"[bold red]{consumed}[/bold red]"
        elif res["budget_consumed_percent"] > 80:
            status = "[bold yellow]WARNING[/bold yellow]"
            consumed = f"[bold yellow]{consumed}[/bold yellow]"
            
        table.add_row(name, total, violations, consumed, status)
        
    console.print(table)

def format_json(results: List[Dict[str, Any]]) -> str:
    return json.dumps({"results": results}, indent=2)

def format_markdown(results: List[Dict[str, Any]]) -> str:
    md = "## API Latency Budget Report\n\n"
    md += "| Endpoint | Total Reqs | Violations | Budget Consumed | Status |\n"
    md += "|---|---|---|---|---|\n"
    
    for res in results:
        status = "🔴 EXHAUSTED" if res["is_exhausted"] else ("🟡 WARNING" if res["budget_consumed_percent"]>80 else "🟢 OK")
        md += f"| {res['name']} | {res['total_requests']} | {res['violations']} | {res['budget_consumed_percent']:.2f}% | {status} |\n"
        
    return md
