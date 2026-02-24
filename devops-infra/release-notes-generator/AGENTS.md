# Release Notes Generator

## Overview
Reads git history between tags and generates polished, categorized release notes.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse git log between tags/commits
- Categorize changes (feat/fix/chore/breaking)
- Generate Markdown release notes
- Include contributor attribution
- Link to PR/issue references
- Auto-detect semantic versioning
- Support conventional commits
- Export to GitHub Releases format

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
