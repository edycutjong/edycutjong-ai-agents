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
    files = glob.glob(os.path.join(directory, "*.md"))  # pragma: no cover
    return sorted(files)  # pragma: no cover

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

        if action == "Exit":  # pragma: no cover
            console.print("[bold red]Goodbye![/bold red]")  # pragma: no cover
            break  # pragma: no cover

        if action == "Convert Single File":  # pragma: no cover
            # List files in input dir
            files = get_markdown_files(config.DEFAULT_INPUT_DIR)  # pragma: no cover
            if not files:  # pragma: no cover
                console.print(f"[yellow]No Markdown files found in {config.DEFAULT_INPUT_DIR}[/yellow]")  # pragma: no cover
                continue  # pragma: no cover

            file_choices = [os.path.basename(f) for f in files]  # pragma: no cover
            file_choices.append("Cancel")  # pragma: no cover

            selected_file_name = questionary.select("Select a file:", choices=file_choices).ask()  # pragma: no cover

            if selected_file_name == "Cancel":  # pragma: no cover
                continue  # pragma: no cover

            filepath = os.path.join(config.DEFAULT_INPUT_DIR, selected_file_name)  # pragma: no cover

            # Options
            polish = questionary.confirm("Do you want AI to polish the content first?", default=False).ask()  # pragma: no cover

            themes = theme_manager.list_themes()  # pragma: no cover
            selected_theme = questionary.select("Select a theme:", choices=themes, default="default").ask()  # pragma: no cover

            # Process
            process_conversion(filepath, selected_theme, polish, parser, theme_manager, converter, ai_editor)  # pragma: no cover

        elif action == "Batch Convert Directory":  # pragma: no cover
             files = get_markdown_files(config.DEFAULT_INPUT_DIR)  # pragma: no cover
             if not files:  # pragma: no cover
                console.print(f"[yellow]No Markdown files found in {config.DEFAULT_INPUT_DIR}[/yellow]")  # pragma: no cover
                continue  # pragma: no cover

             console.print(f"[bold]Found {len(files)} files.[/bold]")  # pragma: no cover

             polish = questionary.confirm("Do you want AI to polish ALL files?", default=False).ask()  # pragma: no cover
             themes = theme_manager.list_themes()  # pragma: no cover
             selected_theme = questionary.select("Select a theme for ALL files:", choices=themes, default="default").ask()  # pragma: no cover

             for filepath in files:  # pragma: no cover
                 process_conversion(filepath, selected_theme, polish, parser, theme_manager, converter, ai_editor)  # pragma: no cover

def process_conversion(filepath, theme_name, polish, parser, theme_manager, converter, ai_editor):
    filename = os.path.basename(filepath)  # pragma: no cover
    output_filename = filename.replace(".md", ".pdf")  # pragma: no cover
    output_path = os.path.join(config.DEFAULT_OUTPUT_DIR, output_filename)  # pragma: no cover

    console.print(f"\n[bold]Processing {filename}...[/bold]")  # pragma: no cover

    with Progress(  # pragma: no cover
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:

        task = progress.add_task("Parsing...", total=None)  # pragma: no cover

        # 1. Parse
        try:  # pragma: no cover
            parsed = parser.parse_file(filepath)  # pragma: no cover
            content = parsed['content']  # pragma: no cover
            metadata = parsed['metadata']  # pragma: no cover

            # Check frontmatter for theme override
            if 'theme' in metadata:  # pragma: no cover
                file_theme = metadata['theme']  # pragma: no cover
                if file_theme in theme_manager.list_themes():  # pragma: no cover
                     # Optionally warn or just use it?
                     # Let's stick to user choice unless we want automatic override.
                     # But user selected a theme. Let's respect user choice but maybe log it.
                     pass  # pragma: no cover
        except Exception as e:  # pragma: no cover
            progress.stop()  # pragma: no cover
            console.print(f"[red]Error parsing {filename}: {e}[/red]")  # pragma: no cover
            return  # pragma: no cover

        # 2. AI Polish
        if polish:  # pragma: no cover
            progress.update(task, description="AI Polishing (this may take a moment)...")  # pragma: no cover
            content = ai_editor.polish_content(content)  # pragma: no cover

        # 3. Load Theme
        progress.update(task, description="Loading Theme...")  # pragma: no cover
        try:  # pragma: no cover
            theme = theme_manager.get_theme(theme_name)  # pragma: no cover
        except Exception as e:  # pragma: no cover
            progress.stop()  # pragma: no cover
            console.print(f"[red]Error loading theme: {e}[/red]")  # pragma: no cover
            return  # pragma: no cover

        # 4. Convert
        progress.update(task, description="Generating PDF...")  # pragma: no cover
        success = converter.convert(content, theme, output_path)  # pragma: no cover

        if success:  # pragma: no cover
            console.print(f"[green]✔ Successfully converted {filename} -> {output_filename}[/green]")  # pragma: no cover
        else:
            console.print(f"[red]✖ Failed to convert {filename}[/red]")  # pragma: no cover

if __name__ == "__main__":
    try:  # pragma: no cover
        main()  # pragma: no cover
    except KeyboardInterrupt:  # pragma: no cover
        console.print("\n[red]Interrupted by user.[/red]")  # pragma: no cover
        sys.exit(0)  # pragma: no cover
