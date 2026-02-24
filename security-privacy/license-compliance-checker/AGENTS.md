# License Compliance Checker

## Overview
Audits project dependencies for license conflicts (GPL vs MIT vs proprietary).

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Scan package.json/requirements.txt/Cargo.toml
- Identify license for each dependency
- Flag incompatible license combinations
- Generate license compliance report
- Detect copyleft contamination risk
- Support SPDX license identifiers
- Export SBOM (Software Bill of Materials)
- Suggest compliant alternatives

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
