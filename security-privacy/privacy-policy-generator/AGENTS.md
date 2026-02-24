# Privacy Policy Generator

## Overview
Reads application code, identifies data collection patterns, and generates GDPR/CCPA-compliant privacy policies.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Scan code for data collection points
- Identify PII handling (email, location, etc.)
- Generate GDPR-compliant privacy policy
- Generate CCPA-compliant privacy policy
- Support multiple output formats (MD/HTML)
- Track third-party data sharing
- Include cookie policy sections
- Version and date policies automatically

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `app.py` — Application entry
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
