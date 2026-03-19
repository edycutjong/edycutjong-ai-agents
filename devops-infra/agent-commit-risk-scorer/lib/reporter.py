import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Dict, Any, List

def format_terminal(score_data: Dict[str, Any], changed_files: List[str]):
    console = Console()
    
    if not changed_files:
        console.print("[bold green]No files changed. Risk Score: 0[/bold green]")
        return
        
    score = score_data["score"]
    
    if score >= 75:
        color = "bold red"
        status = "HIGH RISK"
    elif score >= 40:
        color = "bold yellow"
        status = "MEDIUM RISK"
    else:
        color = "bold green"
        status = "LOW RISK"
        
    console.print(Panel(f"[{color}]Commit Risk Score: {score:.1f}/100 - {status}[/{color}]", title="Analysis Result"))
    
    table = Table(title="Risk Breakdown", show_header=True)
    table.add_column("Vector", style="cyan")
    table.add_column("Score", justify="right")
    
    table.add_row("Criticality", f"{score_data['criticality']:.1f}")
    table.add_row("Blast Radius", f"{score_data['blast_radius']:.1f}")
    table.add_row("Coverage Gap", f"{score_data['coverage_gap']:.1f}")
    table.add_row("Historical Risk", f"{score_data['history_risk']:.1f}")
    table.add_row("Familiarity Discount", f"-{score_data['familiarity_discount']:.1f}", style="green")
    table.add_row("TOTAL", f"[{color}]{score:.1f}[/{color}]")
    
    console.print(table)
    console.print(f"Files Analyzed: {len(changed_files)}")

def format_json(score_data: Dict[str, Any]) -> str:
    return json.dumps(score_data, indent=2)

def format_markdown(score_data: Dict[str, Any], changed_files: List[str]) -> str:
    score = score_data["score"]
    status = "🔴 HIGH RISK" if score >= 75 else ("🟡 MEDIUM RISK" if score >= 40 else "🟢 LOW RISK")
    
    md = f"## Commit Risk Analysis: {status} ({score:.1f}/100)\n\n"
    md += "| Risk Vector | Score |\n"
    md += "|---|---|\n"
    md += f"| Criticality | {score_data['criticality']:.1f} |\n"
    md += f"| Blast Radius | {score_data['blast_radius']:.1f} |\n"
    md += f"| Coverage Gap | {score_data['coverage_gap']:.1f} |\n"
    md += f"| Historical Risk | {score_data['history_risk']:.1f} |\n"
    md += f"| Familiarity Discount | -{score_data['familiarity_discount']:.1f} |\n"
    md += f"| **Total** | **{score:.1f}** |\n\n"
    md += f"*Analyzed {len(changed_files)} files.*\n"
    return md
