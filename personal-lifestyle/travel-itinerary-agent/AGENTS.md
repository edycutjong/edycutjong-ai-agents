# AGENTS.md — Travel Itinerary Agent

## Overview
Plans detailed travel itineraries with costs, routes, accommodations, and activities. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept destination and travel dates
- Research attractions and activities
- Generate day-by-day itinerary
- Estimate daily costs
- Suggest transportation routes
- Include accommodation options
- Add local dining recommendations
- Export as printable PDF/Markdown

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
