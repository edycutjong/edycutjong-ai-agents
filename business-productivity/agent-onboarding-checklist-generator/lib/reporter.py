import json
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

def report_json(checklist: dict) -> str:
    return json.dumps(checklist, indent=2)

def report_markdown(checklist: dict) -> str:
    lines = ["# Developer Onboarding Checklist\n"]
    
    sections = [
        ("Prerequisites", "prerequisites"),
        ("Setup Steps", "setup_steps"),
        ("Verification Steps", "verification_steps")
    ]
    
    for title, key in sections:
        if checklist[key]:
            lines.append(f"## {title}")
            for item in checklist[key]:
                lines.append(f"- [ ] {item}")
            lines.append("")
            
    return "\n".join(lines)

def report_terminal(checklist: dict):
    console = Console(force_terminal=True)
    
    md_content = report_markdown(checklist)
    md = Markdown(md_content)
    
    panel = Panel(
        md,
        title="[bold green]Developer Onboarding Checklist[/bold green]",
        border_style="green"
    )
    console.print(panel)
