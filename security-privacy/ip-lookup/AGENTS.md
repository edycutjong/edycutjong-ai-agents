# IP Lookup

## Overview
IP Lookup — Look up IP address geolocation and network information.

## Tech
- Python 3.10+
- python-dotenv
- pytest

## Features
- Geolocation lookup (city, country)
- ISP and organization info
- Reverse DNS lookup
- IPv4 and IPv6 support
- Batch IP lookups

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
