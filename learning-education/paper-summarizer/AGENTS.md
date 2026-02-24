# Paper Summarizer

## Overview
Reads academic papers (arXiv, etc.) and generates plain-language summaries and key takeaways.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse PDF academic papers
- Extract abstract and methodology
- Generate plain-language summary
- Highlight key findings
- Extract citations and references
- Create visual summary
- Support batch processing
- Generate reading lists by topic

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
