# AGENTS.md — Infrastructure Cost Analyzer

## Overview
Parses cloud billing data (AWS/GCP/Azure), identifies waste, and suggests right-sizing. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse cloud billing CSVs/APIs
- Identify unused resources
- Suggest instance right-sizing
- Calculate potential savings
- Generate cost reports with charts
- Track spending trends over time
- Alert on budget thresholds
- Compare multi-cloud pricing

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
