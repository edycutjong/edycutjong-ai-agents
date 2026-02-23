# AGENTS.md — Spreadsheet Formula Writer

## Overview
Converts natural language questions to Excel/Google Sheets formulas with explanations. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse natural language queries
- Generate Excel formulas (VLOOKUP, INDEX, etc.)
- Generate Google Sheets formulas
- Explain formula logic step-by-step
- Handle complex nested formulas
- Suggest alternatives (XLOOKUP vs VLOOKUP)
- Support array formulas and LAMBDA
- Provide example data demonstrations

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
