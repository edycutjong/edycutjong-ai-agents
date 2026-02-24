# API Response Mocker

## Overview
Reads API specs (OpenAPI/Swagger) and generates mock servers with realistic test data.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse OpenAPI/Swagger specifications
- Generate mock HTTP server
- Return realistic sample responses
- Support dynamic path parameters
- Simulate error responses (4xx/5xx)
- Add configurable latency
- Record and replay requests
- Export as Postman/Insomnia collections

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
