# Test Generator

## Overview
Unit test writer — Analyze function signature.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API
- pytest

## Features
- Analyze function signature
- Generate happy path tests
- Generate edge case tests
- Mock dependencies
- Run generated tests

## File Structure
- `agent_config.py` — Agent configuration
- `config.py` — Configuration & settings
- `example_code.py` — Example Code
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module
- `utils.py` — Utils

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
