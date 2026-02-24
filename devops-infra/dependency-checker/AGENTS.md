# Dependency Checker

## Overview
Dependency Checker — Check project dependencies for outdated or vulnerable packages.

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Check for outdated packages
- Identify known vulnerabilities
- Support pip, npm, and cargo
- Generate dependency reports
- Suggest version updates

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
