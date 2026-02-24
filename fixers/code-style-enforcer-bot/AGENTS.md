# Code Style Enforcer Bot

## Overview
Friendly bot to enforce and fix style.

## Tech
- Python 3.10+
- LangChain
- OpenAI API
- pytest

## Features
- Comment on style vios\n- Auto-fix simple issues\n- Explain rule rationale\n- Detect 'vibe' violations\n- Learn from codebase\n- Gamification stats\n- Custom tone\n- Ignore config

## File Structure
- `agent.py` — Agent
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module
- `tools/` — Tools module
- `utils/` — Utils module

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
