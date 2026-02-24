# Technical Blog Reviewer

## Overview
Reviews technical articles for accuracy, clarity, code correctness, and completeness.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Check technical accuracy of claims
- Validate code snippets run correctly
- Assess readability and structure
- Flag missing context or prerequisites
- Suggest improved explanations
- Check for outdated information
- Score overall article quality
- Generate editorial feedback report

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
- `requirements.txt` — Dependencies
- `tests/` — Tests module
- `ui.py` — Ui

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
