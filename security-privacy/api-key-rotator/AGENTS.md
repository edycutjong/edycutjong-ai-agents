# API Key Rotator

## Overview
Automated secret rotation agent that scans codebases for exposed API keys, tracks key expiration, and assists with secure rotation workflows.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Codebase scanning for exposed secrets
- Key expiration tracking
- Rotation schedule management
- Secure key generation
- Environment file auditing
- Git history secret detection
- Rotation runbook generation
- Integration with secret managers (Vault, AWS SM)

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
