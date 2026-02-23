# AGENTS.md — Database Migration Planner

## Overview
Analyzes database schemas and generates migration plans with rollback strategies. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Compare source and target schemas
- Generate step-by-step migration plan
- Create rollback procedures
- Estimate migration duration
- Identify breaking changes
- Generate migration SQL scripts
- Validate data integrity checks
- Support PostgreSQL/MySQL/SQLite

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
