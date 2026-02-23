# AGENTS.md — Code Explainer

## Overview
Takes complex code snippets and generates line-by-line explanations for learning. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept code in any language
- Generate line-by-line comments
- Explain algorithms step-by-step
- Visualize data flow
- Identify design patterns used
- Explain time/space complexity
- Suggest simplified alternatives
- Support multiple explanation levels

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
