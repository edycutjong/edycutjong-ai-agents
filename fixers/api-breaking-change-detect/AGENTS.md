# API Breaking Change Detect

## Overview
Detect breaking API changes before merge.

## Tech
- Python 3.10+
- LangChain
- OpenAI API
- pytest

## Features
- Compare OpenAPI specs\n- Detect removal/rename\n- Type changes\n- Client impact analysis\n- Version bump suggestion\n- Changelog generation\n- Block PR option\n- Notify consumers

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
