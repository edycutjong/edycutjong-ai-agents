# AGENTS.md — API Doc Generator

## Overview
Reads API route handlers and generates OpenAPI specs with interactive documentation. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse Express/FastAPI/Flask route handlers
- Generate OpenAPI 3.0 specifications
- Create interactive Swagger UI docs
- Extract request/response schemas
- Document authentication requirements
- Generate code examples per endpoint
- Support multiple frameworks
- Auto-detect query/body/path params

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
