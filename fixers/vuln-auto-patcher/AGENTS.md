# Vuln Auto Patcher

## Overview
Auto-patch known security vulnerabilities.

## Tech
- Python 3.10+
- LangChain
- OpenAI API
- pytest

## Features
- Ingest audit report (npm/cve)\n- Find minimal version bump\n- Check breaking changes\n- Run test suite\n- Bisect if failing\n- Create PR\n- Notify security team\n- Lockfile update

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
