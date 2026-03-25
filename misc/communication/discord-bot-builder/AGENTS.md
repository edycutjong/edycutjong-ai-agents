# Discord Bot Builder

## Overview
Agent that generates Discord bot boilerplate code from natural language specifications, including commands, event handlers, and deployment configs.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Natural language to bot code generation
- Slash command scaffolding
- Event handler templates
- Embed builder helpers
- Role management logic
- Database integration (SQLite/Postgres)
- Docker deployment config
- README & documentation generation

## File Structure
- `config.py` — Configuration & settings
- `main.py` — Entry point
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
