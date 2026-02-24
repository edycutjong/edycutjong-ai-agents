# Standup Report Generator

## Overview
Reads git commits and issue trackers, auto-generates daily standup reports.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse recent git commits
- Read Jira/Linear/GitHub issues
- Generate 'Yesterday/Today/Blockers' format
- Summarize code changes in plain English
- Link to relevant PRs and issues
- Support team-wide rollup reports
- Schedule daily generation
- Post to Slack/Teams via webhook

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
