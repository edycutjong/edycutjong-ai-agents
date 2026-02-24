# I18N Missing Key Finder

## Overview
Find missing translation keys.

## Tech
- Python 3.10+
- LangChain
- OpenAI API
- pytest

## Features
- Scan code for tags\n- Compare locale files\n- Identify missing keys\n- Auto-translate (Draft)\n- Find unused keys\n- Consistency check\n- Structure sync\n- Export report

## File Structure
- `README.md` — Documentation
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
