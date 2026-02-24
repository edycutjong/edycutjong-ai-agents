# Regex Builder

## Overview
Takes natural language descriptions and generates, explains, and tests regex patterns.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Convert English to regex patterns
- Explain existing regex step-by-step
- Test regex against sample strings
- Show match groups and captures
- Generate regex for common patterns (email, URL, etc.)
- Support multiple regex flavors (JS, Python, Go)
- Visualize regex as railroad diagram
- Suggest optimized patterns

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
