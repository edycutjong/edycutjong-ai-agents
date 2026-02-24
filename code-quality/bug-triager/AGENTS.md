# Bug Triager

## Overview
Issue management agent — Read new GitHub issues.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Read new GitHub issues
- Label based on content
- Assign to maintainers
- Check for duplicates
- Reply with template

## File Structure
- `agent_config.py` — Agent configuration
- `agents.py` — Agent definitions
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tasks.py` — Task definitions
- `tests/` — Tests module
- `tools.py` — Tool implementations

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
