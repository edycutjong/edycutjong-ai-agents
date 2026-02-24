# File Hash Generator

## Overview
File Hash Generator — Generate file hashes (MD5, SHA-256, SHA-512) for integrity checks.

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Generate MD5, SHA-1, SHA-256 hashes
- SHA-512 support
- Hash file contents or strings
- Compare hash values
- Batch file hashing

## File Structure
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
