# Github Actions Writer

## Overview
Reads project structure and generates optimized GitHub Actions CI/CD workflows.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Detect project language and tools
- Generate CI workflow (lint/test/build)
- Generate CD workflow (deploy)
- Add caching for dependencies
- Configure matrix testing
- Set up release automation
- Add security scanning steps
- Generate reusable workflow files

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
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
