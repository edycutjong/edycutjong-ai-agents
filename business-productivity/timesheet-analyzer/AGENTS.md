# AGENTS.md — Timesheet Analyzer

## Overview
Analyzes time tracking data, identifies productivity patterns, and suggests improvements. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Import timesheet CSV/API data
- Calculate hours per project/client
- Identify productive time patterns
- Detect overtime trends
- Generate utilization reports
- Compare estimated vs actual hours
- Visualize time distribution
- Suggest scheduling improvements

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
