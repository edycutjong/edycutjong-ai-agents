# JSON Schema Generator

## Overview
Analyzes JSON data samples and generates comprehensive JSON Schema definitions.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Infer types from JSON samples
- Generate JSON Schema draft-07/2020-12
- Detect optional vs required fields
- Handle nested objects and arrays
- Generate TypeScript interfaces alongside
- Validate sample data against schema
- Support multiple input samples
- Export schema with descriptions

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
