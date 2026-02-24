# Boilerplate Generator

## Overview
Generates complete project scaffolds (Next.js, Flask, Express) from feature specifications.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept project specifications
- Generate Next.js/React scaffolds
- Generate Flask/FastAPI scaffolds
- Generate Express/Node scaffolds
- Include authentication boilerplate
- Add database connection setup
- Generate environment config files
- Include Docker and CI configs

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
