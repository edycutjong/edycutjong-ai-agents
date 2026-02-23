# AGENTS.md — Chart Generator Agent

## Overview
Takes data and natural language queries, generates chart code (Chart.js, D3, Matplotlib). Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept CSV/JSON data input
- Parse natural language chart requests
- Generate Chart.js configurations
- Generate D3.js visualizations
- Generate Matplotlib/Seaborn plots
- Auto-select appropriate chart type
- Customize colors, labels, axes
- Export as HTML/PNG/SVG

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
