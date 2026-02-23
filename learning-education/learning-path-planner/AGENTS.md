# AGENTS.md — Learning Path Planner

## Overview
Analyzes skill gaps and generates personalized learning roadmaps with resources. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept current skill assessment
- Define target skills and roles
- Generate ordered learning path
- Recommend free/paid resources
- Estimate time per milestone
- Track learning progress
- Suggest projects for practice
- Adjust path based on progress

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
