# AGENTS.md — Workout Planner

## Overview
Creates personalized workout plans based on fitness goals, equipment, and schedule. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept fitness goals and level
- Consider available equipment
- Generate weekly workout schedule
- Include warm-up and cool-down
- Calculate estimated calories burned
- Progress difficulty over time
- Support multiple workout types
- Export as formatted PDF/Markdown

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
