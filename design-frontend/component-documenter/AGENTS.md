# Component Documenter

## Overview
Reads React/Vue/Svelte components and generates Storybook-style documentation.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse component props/types
- Generate interactive examples
- Document component variants
- Create usage guidelines
- Generate prop tables
- Extract JSDoc/TSDoc comments
- Support React/Vue/Svelte/Angular
- Export as MDX/Markdown

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
