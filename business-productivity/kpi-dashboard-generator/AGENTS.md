# AGENTS.md — KPI Dashboard Generator

## Overview
Reads data sources and generates KPI dashboards with configurable alerts. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Connect to CSV/API data sources
- Define KPI metrics and targets
- Generate dashboard HTML/JSON
- Create trend visualizations
- Set up threshold-based alerts
- Support real-time data refresh
- Generate executive summary
- Export as PDF/HTML dashboard

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
