# AGENTS.md — Data Pipeline Validator

## Overview
Validates ETL pipelines, checks data integrity between source and destination systems. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Compare row counts source vs destination
- Validate column types and schemas
- Check for data loss or corruption
- Verify transformation logic
- Generate validation reports
- Support SQL/CSV/Parquet sources
- Schedule recurring validations
- Alert on data quality regressions

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
