# HTML To Markdown

## Overview
HTML to Markdown Converter — Convert HTML content to clean Markdown format.

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Convert HTML tags to Markdown syntax
- Preserve links, images, and formatting
- Handle nested elements and tables
- Clean up whitespace and structure
- Support inline and block elements

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
