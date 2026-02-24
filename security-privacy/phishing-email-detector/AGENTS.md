# Phishing Email Detector

## Overview
Analyzes email headers and content to flag phishing attempts with confidence scores.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse email headers (SPF/DKIM/DMARC)
- Analyze sender reputation
- Detect suspicious URLs and domains
- Identify social engineering patterns
- Score phishing probability
- Extract and check embedded links
- Generate safety report
- Support EML/MSG file formats

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
