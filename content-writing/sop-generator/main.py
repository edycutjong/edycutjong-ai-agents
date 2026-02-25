import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from agent.generator import SOPGenerator
from agent.exporter import SOPExporter

console = Console()

def main():
    console.print(Panel.fit("[bold blue]SOP Generator Agent[/bold blue]\n[italic]Generate standardized operating procedures with AI[/italic]", border_style="blue"))

    if not Config.OPENAI_API_KEY:
        console.print("[bold red]Error:[/bold red] OPENAI_API_KEY not found in environment variables.")
        return

    # Collect inputs
    process_description = Prompt.ask("[bold green]Describe the process/workflow[/bold green]")
    audience = Prompt.ask("[bold green]Target Audience[/bold green]", default="General Staff")

    md_path = None
    pdf_path = None
    full_sop = ""

    try:
        generator = SOPGenerator()
        exporter = SOPExporter()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:

            task = progress.add_task("[cyan]Initializing generator...", total=None)

            progress.update(task, description="[cyan]Generating Title & Metadata...")
            title_meta = generator.generate_title_metadata(process_description)

            progress.update(task, description="[cyan]Generating Purpose & Scope...")
            purpose_scope = generator.generate_purpose_scope(process_description, audience)

            progress.update(task, description="[cyan]Generating Safety & Compliance...")
            safety = generator.generate_safety_compliance(process_description)

            progress.update(task, description="[cyan]Generating Procedure Steps...")
            procedure = generator.generate_procedure_steps(process_description)

            progress.update(task, description="[cyan]Generating Process Diagram...")
            diagram = generator.diagram_generator.generate_mermaid_code(procedure)

            progress.update(task, description="[cyan]Generating Review & Approval...")
            review = generator.generate_review_approval()

            # Combine
            full_sop = (
                f"{title_meta}\n\n"
                f"{purpose_scope}\n\n"
                f"{safety}\n\n"
                f"## Process Flowchart\n{diagram}\n\n"
                f"{procedure}\n\n"
                f"{review}"
            )

            progress.update(task, description="[cyan]Saving files...")

            # Generate filename from title (simple extraction)
            lines = title_meta.split('\n')
            title_line = next((line for line in lines if line.startswith('# ')), "SOP")
            filename_base = title_line.replace('# ', '').strip().replace(' ', '_').lower()
            # Sanitize filename
            filename_base = "".join([c for c in filename_base if c.isalnum() or c in (' ', '_', '-')]).rstrip()

            md_path = exporter.save_markdown(full_sop, filename=f"{filename_base}.md")
            pdf_path = exporter.save_pdf(full_sop, filename=f"{filename_base}.pdf")

        if md_path and pdf_path:
            console.print(Panel(f"[bold green]SOP Generated Successfully![/bold green]\n\nMarkdown: [link=file://{md_path}]{md_path}[/link]\nPDF: [link=file://{pdf_path}]{pdf_path}[/link]", title="Success", border_style="green"))

            # Preview
            console.print("[bold]Preview:[/bold]")
            console.print(Markdown(full_sop))
        else:
             console.print("[bold red]Error:[/bold red] Failed to save files.")

    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()
