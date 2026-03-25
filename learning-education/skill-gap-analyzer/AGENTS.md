# Skill Gap Analyzer

## Overview
Agent that analyzes resumes or skill profiles against job requirements and identifies skill gaps with actionable learning recommendations.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Resume/CV parsing
- Job description analysis
- Skill extraction & matching
- Gap identification with severity
- Learning resource suggestions
- Competitive skill benchmarking
- Industry trend alignment
- PDF report generation

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
