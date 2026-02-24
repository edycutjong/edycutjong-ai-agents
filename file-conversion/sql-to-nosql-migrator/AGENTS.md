# SQL To NOSQL Migrator

## Overview
Converts SQL database schemas to MongoDB/DynamoDB equivalents with migration scripts.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse SQL CREATE TABLE statements
- Design document-based schema
- Handle relationships (embed vs reference)
- Generate MongoDB collection schemas
- Generate DynamoDB table definitions
- Create data migration scripts
- Preserve indexes and constraints
- Generate migration documentation

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
- `pytest.ini` — Pytest configuration
- `requirements.txt` — Dependencies
- `tests/` — Tests module
- `ui/` — Ui module

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
