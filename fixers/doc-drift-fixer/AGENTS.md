# Doc Drift Fixer

## Overview
Aligns documentation with code changes.

## Tech
- Python 3.10+
- LangChain
- OpenAI API
- pytest

## Features
- Connect to Git\n- Analyze PR diffs\n- Scan related docs\n- Propose doc updates\n- Verify code examples\n- Check outdated links\n- Comment on PR\n- Commit changes

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
