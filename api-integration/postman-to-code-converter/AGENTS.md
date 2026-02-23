# AGENTS.md — Postman to Code Converter

## Overview
Converts Postman/Insomnia collections to executable code snippets in any language. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse Postman collection JSON
- Parse Insomnia export files
- Generate Python requests code
- Generate JavaScript fetch/axios code
- Generate cURL commands
- Generate Go HTTP client code
- Preserve authentication headers
- Support environment variable substitution

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
