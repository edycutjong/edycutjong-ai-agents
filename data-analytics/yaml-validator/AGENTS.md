# YAML Validator

## Overview
YAML Validator — Validate YAML files and report syntax errors.

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Validate YAML syntax
- Report line-level errors
- Check for duplicate keys
- Support multi-document YAML
- Pretty-print parsed output

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
