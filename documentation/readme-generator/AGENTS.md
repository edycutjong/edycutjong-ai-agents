# README Generator

## Overview
README Generator — Generate README files from project structure and metadata.

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Generate structured README sections
- Auto-detect project type
- Include installation instructions
- Add badge placeholders
- Support multiple templates

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
