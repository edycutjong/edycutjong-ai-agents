# CSS Dead Code Remover

## Overview
Identify unused CSS selectors.

## Tech
- Python 3.10+
- LangChain
- OpenAI API
- pytest

## Features
- Crawl pages/components\n- Match selectors\n- Identify coverage\n- Purge capabilities\n- Safe-list checking\n- Media query audits\n- Visual regression check\n- Minify

## File Structure
- `agent.py` — Agent
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `templates/` — Templates module
- `tests/` — Tests module
- `tools/` — Tools module
- `verify_crawler.py` — Verify Crawler

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
