# Cron Parser

## Overview
Cron Parser — Parse and explain cron expressions in human-readable format.

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Parse standard cron expressions
- Human-readable explanation
- Show next N run times
- Validate cron syntax
- Support extended cron format

## File Structure
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
