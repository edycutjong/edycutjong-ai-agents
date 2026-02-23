# AGENTS.md — SQL to NoSQL Migrator

## Overview
Converts SQL database schemas to MongoDB/DynamoDB equivalents with migration scripts. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse SQL CREATE TABLE statements
- Design document-based schema
- Handle relationships (embed vs reference)
- Generate MongoDB collection schemas
- Generate DynamoDB table definitions
- Create data migration scripts
- Preserve indexes and constraints
- Generate migration documentation

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
