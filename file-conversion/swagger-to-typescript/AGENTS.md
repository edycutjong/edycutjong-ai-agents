# Swagger To Typescript

## Overview
Generates TypeScript interfaces and API client code from OpenAPI/Swagger specifications.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse OpenAPI 3.0/Swagger 2.0 specs
- Generate TypeScript interfaces
- Create typed API client functions
- Handle nullable and optional fields
- Generate enum types
- Support request/response types
- Create axios/fetch wrappers
- Export as npm package structure

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
