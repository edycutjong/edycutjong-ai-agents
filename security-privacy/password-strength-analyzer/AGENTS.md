# Password Strength Analyzer

## Overview
Evaluates password policies and authentication implementations in codebases.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Analyze password validation logic
- Check against NIST/OWASP guidelines
- Detect weak hashing algorithms
- Flag missing rate limiting
- Review MFA implementation
- Suggest password policy improvements
- Check for credential stuffing protection
- Generate security assessment report

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
