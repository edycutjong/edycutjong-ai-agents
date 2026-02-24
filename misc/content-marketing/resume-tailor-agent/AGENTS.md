# Resume Tailor Agent

## Overview
Agent that tailors your resume/CV for specific job descriptions.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Ingest master resume\n- Ingest job description\n- Rewrite bullet points\n- Optimize keywords\n- Generate cover letter\n- Formatting adjustment\n- PDF export\n- Version tracking

## File Structure
- `agent/` — Agent module
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
