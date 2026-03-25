# GDPR Compliance Checker

## Overview
Privacy compliance agent that scans codebases for PII handling patterns, consent mechanisms, and data retention policy violations.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- PII detection in code & data
- Consent flow analysis
- Data retention policy checker
- Right-to-deletion compliance
- Cookie consent verification
- Privacy policy generator
- DPIA (Data Protection Impact Assessment) template
- Compliance report with GDPR article references

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
