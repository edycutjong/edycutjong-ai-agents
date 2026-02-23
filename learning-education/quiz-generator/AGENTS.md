# AGENTS.md — Quiz Generator

## Overview
Reads educational content and generates multiple-choice and open-ended quizzes. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse educational content (text/PDF)
- Generate multiple-choice questions
- Generate open-ended questions
- Create answer keys with explanations
- Adjust difficulty levels
- Tag questions by topic
- Export as Markdown/JSON
- Generate quiz scoring rubrics

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
