# AGENTS.md — REST to GraphQL Converter

## Overview
Reads REST API endpoint definitions and generates equivalent GraphQL schema and resolvers. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse REST API routes and responses
- Generate GraphQL type definitions
- Create query and mutation schemas
- Generate resolver boilerplate
- Map REST endpoints to GraphQL fields
- Handle nested resource relationships
- Support pagination conversion
- Generate migration guide

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
