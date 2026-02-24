# URL Shortener

## Overview
URL Shortener — Generate shortened URLs and manage link redirects.

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Generate short unique URLs
- Custom alias support
- Track click analytics
- Validate input URLs
- Bulk URL shortening

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
