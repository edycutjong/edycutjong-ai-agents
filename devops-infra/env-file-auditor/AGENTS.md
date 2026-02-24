# Env File Auditor

## Overview
Scans .env files across repositories, detects leaked secrets, duplicates, and missing variables.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Scan repos for .env files
- Detect hardcoded secrets and API keys
- Find duplicate environment variables
- Compare .env vs .env.example
- Flag missing required variables
- Validate variable naming conventions
- Generate .env.example templates
- Check gitignore coverage

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
