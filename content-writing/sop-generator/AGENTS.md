# SOP Generator

## Overview
Reads processes and workflows, generates Standard Operating Procedures with step-by-step instructions.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept process description input
- Generate numbered step-by-step procedures
- Add decision trees for conditional steps
- Include safety/compliance notes
- Generate review and approval workflows
- Add version control metadata
- Include visual aids and diagrams
- Export as formatted Markdown/PDF

## File Structure
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
- `requirements.txt` — Dependencies
- `test_output/` — Test Output module
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
