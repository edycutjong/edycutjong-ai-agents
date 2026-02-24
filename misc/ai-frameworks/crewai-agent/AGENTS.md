# Crewai Agent

## Overview
A multi-agent crew that collaborates to research topics, write reports, and generate insights. Uses CrewAI for agent orchestration.

## Tech
- Python 3.10+
- CrewAI
- OpenAI API

## Features
- 3-agent crew: Researcher, Writer, Editor
- Researcher: searches web, gathers data, extracts key facts
- Writer: synthesizes research into structured report
- Editor: reviews, improves clarity, checks accuracy
- Sequential task execution with handoffs
- Output as formatted markdown report
- Configurable topics via CLI args
- Verbose mode showing agent reasoning

## File Structure
- `README.md` — Documentation
- `agents/` — Agents module
- `cli.py` — Cli
- `config.py` — Configuration & settings
- `crew.py` — Crew
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module
- `tools/` — Tools module

## API Keys
- `OPENAI_API_KEY` — Required

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
