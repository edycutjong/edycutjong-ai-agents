# Postman To Code Converter

## Overview
Converts Postman/Insomnia collections to executable code snippets in any language.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse Postman collection JSON
- Parse Insomnia export files
- Generate Python requests code
- Generate JavaScript fetch/axios code
- Generate cURL commands
- Generate Go HTTP client code
- Preserve authentication headers
- Support environment variable substitution

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
