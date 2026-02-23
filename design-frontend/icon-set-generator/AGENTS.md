# AGENTS.md — Icon Set Generator

## Overview
Generates consistent icon sets from text descriptions using AI. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept icon descriptions
- Generate SVG icons with AI
- Maintain consistent style across set
- Optimize SVG file sizes
- Generate icon sprite sheets
- Create icon font files
- Generate React/Vue icon components
- Export in multiple sizes

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
