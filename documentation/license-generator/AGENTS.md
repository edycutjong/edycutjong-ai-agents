# License Generator

## Overview
License Generator — Generate open-source license files (MIT, Apache, GPL, etc.).

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Generate MIT, Apache 2.0, GPL licenses
- Auto-fill author and year
- Support BSD, ISC, and more
- Preview license text
- Output ready-to-use LICENSE file

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
