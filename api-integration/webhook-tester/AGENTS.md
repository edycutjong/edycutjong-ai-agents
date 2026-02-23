# AGENTS.md — Webhook Tester

## Overview
Creates temporary webhook endpoints, logs incoming payloads, and supports request replay. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Create temporary webhook URLs
- Log incoming request payloads
- Display headers and body
- Replay captured requests
- Filter by method/path/time
- Generate webhook integration docs
- Support custom response codes
- Export captured payloads

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
