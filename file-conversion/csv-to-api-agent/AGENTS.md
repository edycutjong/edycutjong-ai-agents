# CSV To API Agent

## Overview
Takes CSV files and generates REST API servers with CRUD operations automatically.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse CSV column headers and types
- Generate Express/Flask API server
- Create CRUD endpoints per table
- Add filtering and pagination
- Generate API documentation
- Include data validation
- Support SQLite backend
- Hot-reload on data changes

## File Structure
- `agent/` — Agent module
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
