# Rest To GRAPHQL Converter

## Overview
Reads REST API endpoint definitions and generates equivalent GraphQL schema and resolvers.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse REST API routes and responses
- Generate GraphQL type definitions
- Create query and mutation schemas
- Generate resolver boilerplate
- Map REST endpoints to GraphQL fields
- Handle nested resource relationships
- Support pagination conversion
- Generate migration guide

## File Structure
- `README.md` — Documentation
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
