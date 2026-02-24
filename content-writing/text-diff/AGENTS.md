# Text Diff

## Overview
Text Diff Tool — Compare two texts and show their differences line by line.

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Line-by-line diff comparison
- Highlight added and removed content
- Unified diff format output
- Side-by-side comparison
- Ignore whitespace option

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
