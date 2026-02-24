# Config File Generator

## Overview
Generates ESLint, Prettier, TSConfig, and other config files from project conventions.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Detect project language and framework
- Generate ESLint configuration
- Generate Prettier configuration
- Generate tsconfig.json
- Generate .editorconfig
- Generate husky/lint-staged configs
- Support monorepo configs
- Apply opinionated best practices

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
