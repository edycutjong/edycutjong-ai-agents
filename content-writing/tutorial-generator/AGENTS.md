# Tutorial Generator

## Overview
Reads code libraries and generates step-by-step tutorials with runnable examples.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Analyze library API surface
- Generate beginner-friendly tutorials
- Create step-by-step instructions
- Include runnable code examples
- Add prerequisite checklist
- Generate troubleshooting section
- Support multiple difficulty levels
- Export as Markdown with code blocks

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
