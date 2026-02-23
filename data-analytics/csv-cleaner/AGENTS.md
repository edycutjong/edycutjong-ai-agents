# AGENTS.md — CSV Cleaner

## Overview
Ingests messy CSV files, detects and fixes encoding issues, duplicates, missing values, and type mismatches. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Detect and fix file encoding issues
- Remove duplicate rows (exact and fuzzy)
- Handle missing values (fill/drop/interpolate)
- Standardize date and number formats
- Fix column type mismatches
- Remove trailing whitespace and newlines
- Generate data quality report
- Export cleaned CSV with changelog

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
