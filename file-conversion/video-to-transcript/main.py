import argparse
import sys
import os
from rich.console import Console
from rich.progress import Progress

# Ensure the current directory is in sys.path (it usually is when running as script)
# But for safety in different execution contexts:
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)  # pragma: no cover

try:
    from config import Config
    from agent.utils import extract_audio
    from agent.transcriber import Transcriber
    from agent.analysis import ContentAnalyzer
except ImportError as e:  # pragma: no cover
    # If running as a module/package from root, we might need relative imports or different path setup
    # But given the hyphens in path, local imports are best when running the script directly.
    print(f"Import Error: {e}")  # pragma: no cover
    print("Please run this script directly from its directory or ensure the path is correct.")  # pragma: no cover
    sys.exit(1)  # pragma: no cover

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Video to Transcript Converter")
    parser.add_argument("input_file", help="Path to video or audio file")
    parser.add_argument("--format", default="markdown", choices=["markdown", "srt", "vtt", "json", "text"], help="Output format")
    parser.add_argument("--language", help="Language code (e.g. 'en')")
    parser.add_argument("--analyze", action="store_true", help="Generate summary and chapters (only for markdown format)")
    parser.add_argument("--api-key", help="OpenAI API Key")

    args = parser.parse_args()

    api_key = args.api_key or Config.OPENAI_API_KEY
    if not api_key:
        console.print("[red]Error: OpenAI API Key is required. Set OPENAI_API_KEY env var or use --api-key.[/red]")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    input_path = args.input_file
    if not os.path.exists(input_path):
        console.print(f"[red]Error: File {input_path} not found.[/red]")
        sys.exit(1)

    with Progress() as progress:
        task1 = progress.add_task("[cyan]Processing...", total=3)

        # 1. Extract Audio
        progress.update(task1, description="[cyan]Extracting Audio...[/cyan]")
        temp_audio_filename = f"temp_{os.path.basename(input_path)}.mp3"
        temp_audio_path = os.path.join(Config.TEMP_DIR, temp_audio_filename)
        try:
            audio_path = extract_audio(input_path, temp_audio_path)
        except Exception as e:
             console.print(f"[red]Extraction failed: {e}[/red]")
             sys.exit(1)
        progress.advance(task1)  # pragma: no cover

        # 2. Transcribe
        progress.update(task1, description="[cyan]Transcribing...[/cyan]")  # pragma: no cover
        try:  # pragma: no cover
            transcriber = Transcriber(api_key=api_key)  # pragma: no cover
        except ValueError as e:  # pragma: no cover
            console.print(f"[red]{e}[/red]")  # pragma: no cover
            sys.exit(1)  # pragma: no cover

        # Determine format for whisper
        whisper_format = "text"  # pragma: no cover
        if args.format in ["srt", "vtt", "json"]:  # pragma: no cover
            whisper_format = args.format  # pragma: no cover
        elif args.format == "markdown":  # pragma: no cover
            whisper_format = "text" # We'll format manually  # pragma: no cover

        try:  # pragma: no cover
            transcript_result = transcriber.transcribe(audio_path, response_format=whisper_format, language=args.language)  # pragma: no cover
        except Exception as e:  # pragma: no cover
            console.print(f"[red]Transcription failed: {e}[/red]")  # pragma: no cover
            sys.exit(1)  # pragma: no cover

        progress.advance(task1)  # pragma: no cover

        # 3. Analyze (Optional)
        final_output = ""  # pragma: no cover
        if args.analyze and args.format == "markdown":  # pragma: no cover
            progress.update(task1, description="[cyan]Analyzing...[/cyan]")  # pragma: no cover
            try:  # pragma: no cover
                analyzer = ContentAnalyzer(api_key=api_key)  # pragma: no cover

                transcript_text = transcript_result if isinstance(transcript_result, str) else str(transcript_result)  # pragma: no cover
                summary = analyzer.summarize(transcript_text)  # pragma: no cover
                chapters = analyzer.generate_chapters(transcript_text)  # pragma: no cover

                final_output = f"# Transcript\n\n## Summary\n{summary}\n\n## Chapters\n{chapters}\n\n## Full Text\n{transcript_text}"  # pragma: no cover
            except Exception as e:  # pragma: no cover
                console.print(f"[yellow]Analysis failed: {e}. Saving raw transcript only.[/yellow]")  # pragma: no cover
                final_output = transcript_result if isinstance(transcript_result, str) else str(transcript_result)  # pragma: no cover
        else:
             final_output = transcript_result if isinstance(transcript_result, str) else str(transcript_result)  # pragma: no cover

        progress.advance(task1)  # pragma: no cover

    # Save Output
    ext_map = {"markdown": "md", "text": "txt", "json": "json", "srt": "srt", "vtt": "vtt"}  # pragma: no cover
    output_filename = os.path.splitext(os.path.basename(input_path))[0] + f"_transcript.{ext_map.get(args.format, 'txt')}"  # pragma: no cover
    output_path = os.path.join(Config.OUTPUT_DIR, output_filename)  # pragma: no cover

    with open(output_path, "w", encoding="utf-8") as f:  # pragma: no cover
        f.write(final_output)  # pragma: no cover

    console.print(f"[green]Success! Transcript saved to: {output_path}[/green]")  # pragma: no cover

if __name__ == "__main__":
    main()
