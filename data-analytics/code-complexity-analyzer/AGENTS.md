# Code Complexity Analyzer

## Overview
Code Complexity Analyzer — Analyze code complexity metrics (cyclomatic complexity, LOC, etc.).

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Calculate cyclomatic complexity
- Count lines of code (LOC)
- Identify complex functions
- Generate complexity reports
- Support multiple languages

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
