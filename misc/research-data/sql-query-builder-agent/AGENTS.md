# SQL Query Builder Agent

## Overview
Natural language to SQL agent. Connects to schema, writes safe queries.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Schema introspection\n- Question answering\n- Query generation\n- Explain query plan\n- Optimization suggestions\n- Read-only mode enforcement\n- Multi-dialect support\n- Visual result preview

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
- `requirements.txt` — Dependencies
- `sample_data.db` — Sample Data.Db
- `tests/` — Tests module
- `utils/` — Utils module

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
