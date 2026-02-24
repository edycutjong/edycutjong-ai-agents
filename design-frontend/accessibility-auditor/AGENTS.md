# Accessibility Auditor

## Overview
Scans HTML pages for WCAG 2.1 violations and generates prioritized fix suggestions.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Run automated WCAG 2.1 checks
- Check color contrast ratios
- Validate ARIA label usage
- Test keyboard navigation flow
- Check image alt text coverage
- Validate form label associations
- Generate prioritized fix list
- Score overall accessibility level

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
