# AGENTS.md — Habit Coach

## Overview
Tracks daily habits, analyzes patterns, provides motivational nudges and streak tracking. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Define trackable habits
- Log daily completions
- Calculate streaks and chains
- Analyze completion patterns
- Generate motivational reminders
- Visualize habit heatmaps
- Identify best/worst days
- Generate weekly progress reports

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
