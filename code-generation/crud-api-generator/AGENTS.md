# AGENTS.md — CRUD API Generator

## Overview
Reads database schemas and generates full CRUD API with validation and documentation. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse database schema (SQL/Prisma)
- Generate REST endpoints (CRUD)
- Add input validation rules
- Generate API documentation
- Include error handling
- Add pagination and filtering
- Generate test files
- Support Express/FastAPI/Flask

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
