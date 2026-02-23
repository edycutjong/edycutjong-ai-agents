# AGENTS.md — Migration File Writer

## Overview
Compares old and new database schemas, generates migration files for popular ORMs. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Compare before/after schemas
- Generate Prisma migration files
- Generate Alembic migration scripts
- Generate Knex migration files
- Handle add/remove/modify columns
- Preserve existing data strategies
- Generate rollback scripts
- Validate migration safety

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
