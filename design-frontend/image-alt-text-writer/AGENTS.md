# AGENTS.md — Image Alt Text Writer

## Overview
Scans HTML for images missing alt text and generates descriptive alternatives using AI. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Scan HTML files for img tags
- Detect missing alt attributes
- Generate descriptive alt text with AI
- Handle decorative vs informative images
- Check alt text quality/length
- Generate accessibility report
- Batch process multiple pages
- Support multiple languages

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
