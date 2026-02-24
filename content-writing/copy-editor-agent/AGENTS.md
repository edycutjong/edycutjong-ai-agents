# Copy Editor Agent

## Overview
Proofreads text for grammar, style, tone consistency, and readability score.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Check grammar and spelling
- Enforce style guide rules (AP/Chicago)
- Analyze reading level (Flesch-Kincaid)
- Detect passive voice overuse
- Suggest concise alternatives
- Check tone consistency
- Flag jargon and acronyms
- Generate editing summary report

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
