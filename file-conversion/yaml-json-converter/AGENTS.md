# YAML JSON Converter

## Overview
Bi-directional YAML-to-JSON conversion with validation, comments preservation, and formatting.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Convert YAML to JSON
- Convert JSON to YAML
- Preserve YAML comments where possible
- Validate against schemas
- Format with configurable indentation
- Handle multi-document YAML
- Support anchors and aliases
- Batch convert directory of files

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
