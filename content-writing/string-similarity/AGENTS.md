# String Similarity

## Overview
String Similarity Analyzer — Compare two strings and calculate their similarity score.

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Calculate similarity percentage
- Support multiple comparison algorithms
- Highlight differences between strings
- Handle Unicode and special characters
- Batch comparison support

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
