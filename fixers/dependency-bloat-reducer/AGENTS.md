# Dependency Bloat Reducer

## Overview
Find heavy/unused dependencies.

## Tech
- Python 3.10+
- LangChain
- OpenAI API
- pytest

## Features
- Analyze bundle size\n- Cost per package\n- Find unused exports\n- Suggest lighter alternatives\n- Tree-shaking audit\n- Duplicate package check\n- Visualize graph\n- Remove generation

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
