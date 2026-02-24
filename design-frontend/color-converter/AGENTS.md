# Color Converter

## Overview
Color Converter — Convert between color formats (HEX, RGB, HSL).

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Convert HEX to RGB and HSL
- Convert RGB to HEX and HSL
- Convert HSL to HEX and RGB
- Color name lookup
- Batch color conversion

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
