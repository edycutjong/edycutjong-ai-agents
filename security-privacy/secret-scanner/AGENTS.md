# Secret Scanner

## Overview
Deep-scans repositories for leaked API keys, passwords, tokens, and certificates.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Scan files for secret patterns (regex)
- Detect API keys across 50+ providers
- Find hardcoded passwords and tokens
- Check git history for leaked secrets
- Generate remediation report
- Suggest secret rotation steps
- Support custom secret patterns
- Pre-commit hook integration

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
