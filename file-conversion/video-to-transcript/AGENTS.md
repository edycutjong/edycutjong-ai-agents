# Video To Transcript

## Overview
Transcribes video and audio files, generating timestamped Markdown transcripts.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept video/audio file input
- Transcribe speech to text
- Add timestamps per segment
- Identify speaker changes
- Generate Markdown transcript
- Create chapter markers
- Support multiple languages
- Export as SRT/VTT subtitles

## File Structure
- `README.md` — Documentation
- `__init__.py` — Package init
- `agent/` — Agent module
- `app.py` — Application entry
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `output/` — Output module
- `prompts/` — Prompts module
- `requirements.txt` — Dependencies
- `temp/` — Temp module
- `tests/` — Tests module

## API Keys
- `GEMINI_API_KEY` — Required

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
