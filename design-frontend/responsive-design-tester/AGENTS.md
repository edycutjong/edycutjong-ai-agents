# Responsive Design Tester

## Overview
Screenshots web pages at multiple viewports and flags layout issues automatically.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Capture screenshots at multiple breakpoints
- Detect layout overflow issues
- Flag text truncation problems
- Check touch target sizes on mobile
- Compare against design mockups
- Generate responsive audit report
- Support custom viewport sizes
- Test horizontal scrolling issues

## File Structure
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
