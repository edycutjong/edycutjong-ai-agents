# Deprecation Hunter

## Overview
Finds and intends to fix deprecated usage.

## Tech
- Python 3.10+
- LangChain
- OpenAI API
- pytest

## Features
- Scan dependencies\n- Find deprecated calls\n- Suggest replacements\n- Generate refactor PR\n- Safety check tests\n- Group by library\n- Priority sorting\n- Report generation

## File Structure
- `agent.py` — Agent
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module
- `tools/` — Tools module

## API Keys
- `OPENAI_API_KEY` — Required

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
