# AGENTS.md — OKR Tracker

## Overview
Manages Objectives and Key Results, tracks progress, and generates status reports. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Define objectives and key results
- Track progress percentages
- Generate weekly status reports
- Calculate team OKR scores
- Alert on at-risk objectives
- Visualize progress over time
- Support quarterly cycles
- Export reports as Markdown

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
