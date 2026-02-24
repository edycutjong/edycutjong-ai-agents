# Unused Asset Cleaner

## Overview
Find and remove unused images/files.

## Tech
- Python 3.10+
- LangChain
- OpenAI API
- pytest

## Features
- Scan source code\n- Scan asset folders\n- Graph dependencies\n- Identify orphans\n- Move to trash/backup\n- Confirm before delete\n- Optimize remaining\n- Report savings

## File Structure
- `agent.py` — Agent
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module
- `tools/` — Tools module

## API Keys
- `OPENAI_API_KEY` — Required

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
