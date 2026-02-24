# Uuid Generator

## Overview
UUID Generator — Generate and validate UUIDs (v1, v4, v5).

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Generate UUID v1, v4, and v5
- Validate UUID format
- Batch generation support
- Namespace-based UUID v5
- Copy-ready output

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
