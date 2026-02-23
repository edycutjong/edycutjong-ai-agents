# AGENTS.md — Video to Transcript

## Overview
Transcribes video and audio files, generating timestamped Markdown transcripts. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

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
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings
- `requirements.txt`: Dependencies
- `tests/`: Test files

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
