# AGENTS.md — GraphQL Schema Analyzer

## Overview
Analyzes GraphQL schemas, suggests optimizations, and detects N+1 query problems. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse GraphQL SDL schemas
- Detect N+1 query patterns
- Identify unused types and fields
- Suggest query complexity limits
- Analyze resolver patterns
- Generate schema documentation
- Recommend pagination strategies
- Flag circular type references

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
