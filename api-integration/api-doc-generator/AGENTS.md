# API Doc Generator

## Overview
Reads API route handlers and generates OpenAPI specs with interactive documentation.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse Express/FastAPI/Flask route handlers
- Generate OpenAPI 3.0 specifications
- Create interactive Swagger UI docs
- Extract request/response schemas
- Document authentication requirements
- Generate code examples per endpoint
- Support multiple frameworks
- Auto-detect query/body/path params

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
