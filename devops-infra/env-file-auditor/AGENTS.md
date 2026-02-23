# AGENTS.md — Env File Auditor

## Overview
Scans .env files across repositories, detects leaked secrets, duplicates, and missing variables. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Scan repos for .env files
- Detect hardcoded secrets and API keys
- Find duplicate environment variables
- Compare .env vs .env.example
- Flag missing required variables
- Validate variable naming conventions
- Generate .env.example templates
- Check gitignore coverage

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
