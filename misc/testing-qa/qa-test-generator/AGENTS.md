# QA Test Generator

## Overview
Agent that reads features/code and generates Cypress/Playwright tests.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Parse UI components\n- Generate test scenarios\n- Write executable test code\n- Mock API responses\n- Self-healing tests (update selectors)\n- Integration with test runner\n- Coverage analysis\n- Edge case generation

## File Structure
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
- `requirements.txt` — Dependencies
- `tests/` — Tests module

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
