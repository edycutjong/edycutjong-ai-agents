# AGENTS.md — Uptime Monitor Agent

## Overview
Polls HTTP endpoints, detects downtime, and sends alerts with diagnostic context. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Poll configurable endpoints at intervals
- Check HTTP status codes and response times
- Detect SSL certificate expiry
- Send alerts via webhook/email
- Generate uptime percentage reports
- Record response time history
- Support custom health check logic
- Dashboard with status page output

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
