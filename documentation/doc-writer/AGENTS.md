# Doc Writer

## Overview
Documentation generator — Parse codebase AST.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse codebase AST
- Generate docstrings/README
- Identify missing docs
- Update outdated docs
- Follow style guide

## File Structure
- `config.py` — Configuration & settings
- `doc_writer/` — Doc Writer module
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module

## API Keys
- `GEMINI_API_KEY` — Required

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
