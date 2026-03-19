import json
from typing import Dict, Any, List
from rich.table import Table

def format_json(drifts: Dict[str, List[Dict[str, Any]]]) -> str:
    """Formats the drift results as a JSON string."""
    return json.dumps(drifts, indent=2)

def format_markdown(drifts: Dict[str, List[Dict[str, Any]]]) -> str:
    """Formats the drift results as a Markdown table."""
    if not drifts:
        return "✅ No schema drift detected.\n"
        
    md = "## Schema Drift Report\n\n"
    md += "| Table | Issue Type | Field | Details |\n"
    md += "|-------|------------|-------|---------|\n"
    
    for table, issues in drifts.items():
        for issue in issues:
            field = issue.get("field", "-")
            md += f"| `{table}` | {issue['type']} | `{field}` | {issue['details']} |\n"
            
    return md

def format_table(drifts: Dict[str, List[Dict[str, Any]]]) -> Table:
    """Formats the drift results as a Rich Table."""
    table = Table(title="Schema Drift Report")
    table.add_column("Table", style="cyan")
    table.add_column("Issue Type", style="red")
    table.add_column("Field", style="magenta")
    table.add_column("Details", style="yellow", no_wrap=False)
    
    if not drifts:
        table.add_row("All Good", "None", "-", "No schema drift detected.")
        return table
        
    for table_name, issues in drifts.items():
        for issue in issues:
            field = issue.get("field") or "-"
            table.add_row(table_name, issue["type"], field, issue["details"])
            
    return table
