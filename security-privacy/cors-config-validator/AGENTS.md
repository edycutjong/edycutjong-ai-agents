# CORS Config Validator

## Overview
Analyzes CORS configurations across APIs, flags overly permissive or broken setups.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse CORS headers from responses
- Detect wildcard origin allowances
- Flag missing credentials handling
- Test preflight request behavior
- Identify mismatched configurations
- Suggest restrictive CORS policies
- Generate configuration templates
- Support Express/Django/FastAPI configs

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
