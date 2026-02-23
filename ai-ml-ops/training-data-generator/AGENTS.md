# AGENTS.md — Training Data Generator

## Overview
Generates synthetic training data from specifications and seed examples. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept data schema and examples
- Generate diverse synthetic samples
- Maintain statistical distribution
- Support text/tabular/image metadata
- Export in JSONL/CSV/Parquet formats
- Apply data augmentation techniques
- Validate generated data quality
- Scale to configurable dataset sizes

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
