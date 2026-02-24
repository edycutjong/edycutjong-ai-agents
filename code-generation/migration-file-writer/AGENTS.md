# Migration File Writer

## Overview
Compares old and new database schemas, generates migration files for popular ORMs.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Compare before/after schemas
- Generate Prisma migration files
- Generate Alembic migration scripts
- Generate Knex migration files
- Handle add/remove/modify columns
- Preserve existing data strategies
- Generate rollback scripts
- Validate migration safety

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `app.py` — Application entry
- `config.py` — Configuration & settings
- `main.py` — Entry point
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
