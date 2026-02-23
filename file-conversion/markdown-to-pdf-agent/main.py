import os
import sys
import glob
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
import questionary

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.parser import MarkdownParser
from agent.theme_manager import ThemeManager
from agent.converter import PDFConverter
from agent.ai_editor import AIEditor
import config

console = Console()

def print_header():
    title = Text("Markdown to PDF Agent", style="bold cyan")
    subtitle = Text("Convert • Polish • Style", style="italic white")
    console.print(Panel.fit(Text.assemble(title, "\n", subtitle), border_style="cyan", padding=(1, 2)))

def get_markdown_files(directory):
    files = glob.glob(os.path.join(directory, "*.md"))
    return sorted(files)

def main():
    print_header()

    parser = MarkdownParser()
    theme_manager = ThemeManager()
    converter = PDFConverter()
    ai_editor = AIEditor(api_key=config.OPENAI_API_KEY, model=config.DEFAULT_MODEL)

    while True:
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "Convert Single File",
                "Batch Convert Directory",
                "Exit"
            ],
            style=questionary.Style([
                ('qmark', 'fg:#00ffff bold'),
                ('question', 'bold'),
                ('answer', 'fg:#f44336 bold'),
                ('pointer', 'fg:#673ab7 bold'),
                ('highlighted', 'fg:#673ab7 bold'),
                ('selected', 'fg:#cc5454'),
                ('separator', 'fg:#cc5454'),
                ('instruction', ''),
                ('text', ''),
                ('disabled', 'fg:#858585 italic')
            ])
        ).ask()

        if action == "Exit":
            console.print("[bold red]Goodbye![/bold red]")
            break

        if action == "Convert Single File":
            # List files in input dir
            files = get_markdown_files(config.DEFAULT_INPUT_DIR)
            if not files:
                console.print(f"[yellow]No Markdown files found in {config.DEFAULT_INPUT_DIR}[/yellow]")
                continue

            file_choices = [os.path.basename(f) for f in files]
            file_choices.append("Cancel")

            selected_file_name = questionary.select("Select a file:", choices=file_choices).ask()

            if selected_file_name == "Cancel":
                continue

            filepath = os.path.join(config.DEFAULT_INPUT_DIR, selected_file_name)

            # Options
            polish = questionary.confirm("Do you want AI to polish the content first?", default=False).ask()

            themes = theme_manager.list_themes()
            selected_theme = questionary.select("Select a theme:", choices=themes, default="default").ask()

            # Process
            process_conversion(filepath, selected_theme, polish, parser, theme_manager, converter, ai_editor)

        elif action == "Batch Convert Directory":
             files = get_markdown_files(config.DEFAULT_INPUT_DIR)
             if not files:
                console.print(f"[yellow]No Markdown files found in {config.DEFAULT_INPUT_DIR}[/yellow]")
                continue

             console.print(f"[bold]Found {len(files)} files.[/bold]")

             polish = questionary.confirm("Do you want AI to polish ALL files?", default=False).ask()
             themes = theme_manager.list_themes()
             selected_theme = questionary.select("Select a theme for ALL files:", choices=themes, default="default").ask()

             for filepath in files:
                 process_conversion(filepath, selected_theme, polish, parser, theme_manager, converter, ai_editor)

def process_conversion(filepath, theme_name, polish, parser, theme_manager, converter, ai_editor):
    filename = os.path.basename(filepath)
    output_filename = filename.replace(".md", ".pdf")
    output_path = os.path.join(config.DEFAULT_OUTPUT_DIR, output_filename)

    console.print(f"\n[bold]Processing {filename}...[/bold]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:

        task = progress.add_task("Parsing...", total=None)

        # 1. Parse
        try:
            parsed = parser.parse_file(filepath)
            content = parsed['content']
            metadata = parsed['metadata']

            # Check frontmatter for theme override
            if 'theme' in metadata:
                file_theme = metadata['theme']
                if file_theme in theme_manager.list_themes():
                     # Optionally warn or just use it?
                     # Let's stick to user choice unless we want automatic override.
                     # But user selected a theme. Let's respect user choice but maybe log it.
                     pass
        except Exception as e:
            progress.stop()
            console.print(f"[red]Error parsing {filename}: {e}[/red]")
            return

        # 2. AI Polish
        if polish:
            progress.update(task, description="AI Polishing (this may take a moment)...")
            content = ai_editor.polish_content(content)

        # 3. Load Theme
        progress.update(task, description="Loading Theme...")
        try:
            theme = theme_manager.get_theme(theme_name)
        except Exception as e:
            progress.stop()
            console.print(f"[red]Error loading theme: {e}[/red]")
            return

        # 4. Convert
        progress.update(task, description="Generating PDF...")
        success = converter.convert(content, theme, output_path)

        if success:
            console.print(f"[green]✔ Successfully converted {filename} -> {output_filename}[/green]")
        else:
            console.print(f"[red]✖ Failed to convert {filename}[/red]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Interrupted by user.[/red]")
        sys.exit(0)
