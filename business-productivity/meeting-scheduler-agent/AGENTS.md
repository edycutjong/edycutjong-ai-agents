# AGENTS.md — Meeting Scheduler Agent

## Overview
Finds optimal meeting times across calendars and time zones using AI. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept participant availability
- Handle multiple time zones
- Find optimal meeting slots
- Respect working hours preferences
- Suggest multiple options ranked
- Generate calendar invites
- Handle recurring meetings
- Integrate with Google/Outlook calendars

## File Structure
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings
- `requirements.txt`: Dependencies
- `tests/`: Test files

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
