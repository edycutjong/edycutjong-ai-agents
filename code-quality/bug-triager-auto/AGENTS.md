# Bug Triager Auto

## Overview
Agent that analyzes incoming bug reports, duplicates, and assigns severity.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Read issue tracker\n- Detect duplicates/similar issues\n- Assign labels/severity\n- Request missing info\n- Suggest potential fix files\n- Route to correct team\n- Sentiment analysis\n- Close stale issues

## File Structure
- `README.md` — Documentation
- `__init__.py` — Package init
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `mock_data.json` — Mock Data.Json
- `prompts/` — Prompts module
- `requirements.txt` — Dependencies
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
