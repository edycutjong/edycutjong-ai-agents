# Research Summarizer Agent

## Overview
Deep research agent. Give a topic, it browses, reads, and synthesizes a report.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Multi-step web browsing\n- Source citation\n- Synthesize multiple sources\n- Generate PDF/Markdown report\n- Fact checking step\n- Configurable depth\n- Specific domain filtering\n- Save research history

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `poetry.lock` — Poetry.Lock
- `prompts/` — Prompts module
- `pyproject.toml` — Project configuration
- `requirements.txt` — Dependencies
- `research_history/` — Research History module
- `tests/` — Tests module
- `utils/` — Utils module

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
