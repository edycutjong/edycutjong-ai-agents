# Log Noise Reducer

## Overview
Identify spammy logs to cleanup.

## Tech
- Python 3.10+
- LangChain
- OpenAI API
- pytest

## Features
- Analyze production logs\n- Find high volume\n- Identify source line\n- Suggest level change (Info->Debug)\n- Remove print statements\n- Sampling suggestion\n- Cost impact\n- Jira creation

## File Structure
- `agent.py` — Agent
- `config.py` — Configuration & settings
- `dummy_app.py` — Dummy A
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
