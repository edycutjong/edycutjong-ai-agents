# Meeting Notes Organizer

## Overview
Agent that takes transcripts, extracts tasks, and updates project management tools.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Transcript ingestion\n- Summary generation\n- Action item extraction\n- API integration (Jira/Linear)\n- Calendar event creation\n- Follow-up email draft\n- Speaker diarization support\n- Searchable archive

## File Structure
- `README.md` — Documentation
- `__init__.py` — Package init
- `agent/` — Agent module
- `cli.py` — Cli
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
- `requirements.txt` — Dependencies
- `style.css` — Style.Css
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
