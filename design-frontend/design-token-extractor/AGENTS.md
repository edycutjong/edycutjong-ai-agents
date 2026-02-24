# Design Token Extractor

## Overview
Reads Figma files or design specs and generates CSS/SCSS design token variables.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse Figma/Sketch design files
- Extract colors, fonts, spacing
- Generate CSS custom properties
- Generate SCSS variables
- Generate Tailwind theme config
- Create consistent naming conventions
- Support light/dark themes
- Export as JSON token format

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
