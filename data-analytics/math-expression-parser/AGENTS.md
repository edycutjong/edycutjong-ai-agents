# Math Expression Parser

## Overview
Math Expression Parser — Parse and evaluate mathematical expressions safely.

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Evaluate arithmetic expressions
- Support parentheses and operator precedence
- Handle trigonometric functions
- Variable substitution
- Step-by-step evaluation

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
