# AGENTS.md — CSV to API Agent

## Overview
Takes CSV files and generates REST API servers with CRUD operations automatically. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse CSV column headers and types
- Generate Express/Flask API server
- Create CRUD endpoints per table
- Add filtering and pagination
- Generate API documentation
- Include data validation
- Support SQLite backend
- Hot-reload on data changes

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
