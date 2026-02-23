# AGENTS.md — Competitive Analysis Agent

## Overview
Researches competitors, compares features and pricing, generates analysis reports. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Research competitor websites
- Compare feature sets
- Analyze pricing strategies
- Identify market positioning
- Generate SWOT analysis
- Track competitor changes over time
- Create comparison matrices
- Export as presentation-ready report

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
