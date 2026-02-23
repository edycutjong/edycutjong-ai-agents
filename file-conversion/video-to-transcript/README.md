# Video to Transcript Agent

A premium file conversion tool that extracts audio from videos, transcribes it using OpenAI Whisper, and generates summaries and chapter markers using LangChain.

## Features

- **Video/Audio Input:** Supports mp4, mov, avi, mp3, wav, etc.
- **Transcription:** High-accuracy transcription using OpenAI Whisper API.
- **Analysis:** Generates a concise summary and timestamped chapter markers.
- **Formats:** Exports to Markdown, Text, JSON, SRT, VTT.
- **Premium UI:** Streamlit-based interface with dark mode.
- **CLI:** Robust command-line interface for batch processing.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your OpenAI API Key:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   # Or set it in .env file
   ```

## Usage

### Streamlit UI (Recommended)

Run the premium UI:
```bash
streamlit run app.py
```

### CLI

Run the command-line tool:
```bash
python main.py input_video.mp4 --format markdown --analyze
```

**Options:**
- `--format`: Output format (markdown, srt, vtt, json, text). Default: markdown.
- `--language`: Language code (e.g. `en`). Optional.
- `--analyze`: Enable AI summary and chapter generation (Markdown only).
- `--api-key`: Provide API key directly.

## Structure

- `app.py`: Streamlit UI entry point.
- `main.py`: CLI entry point.
- `agent/`: Core logic (Transcription, Analysis, Utils).
- `prompts/`: AI prompts for analysis.
- `tests/`: Unit tests.

## Testing

Run tests with pytest:
```bash
pytest tests/
```
