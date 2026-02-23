# AGENTS.md — API Changelog Differ

## Overview
Compares API versions (OpenAPI specs), generates detailed migration guides. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Compare two OpenAPI spec versions
- Detect added/removed/changed endpoints
- Identify breaking changes
- Generate migration guide
- Categorize changes by severity
- Create developer changelog
- Support JSON/YAML specs
- Highlight deprecated endpoints

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
