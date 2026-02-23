# AGENTS.md — Data Faker Agent

## Overview
Generates realistic fake seed data matching schema definitions for testing. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Read database schema or JSON Schema
- Generate contextually realistic data
- Support locale-specific formats
- Handle relationships and foreign keys
- Generate configurable row counts
- Export as SQL INSERT/CSV/JSON
- Maintain referential integrity
- Support custom field generators

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
