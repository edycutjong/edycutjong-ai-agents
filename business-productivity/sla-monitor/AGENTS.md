# AGENTS.md — SLA Monitor

## Overview
Tracks SLA compliance, calculates uptime percentages, and alerts on breaches. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Define SLA targets per service
- Calculate uptime percentages
- Track response time SLAs
- Generate compliance reports
- Alert on SLA breaches
- Historical trend analysis
- Support multiple SLA tiers
- Export reports for stakeholders

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
