# AGENTS.md — Interview Prep Agent

## Overview
Generates technical interview questions based on job descriptions and tech stacks. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse job description
- Identify required skills and technologies
- Generate coding challenges
- Create system design questions
- Generate behavioral questions (STAR)
- Provide sample answers
- Grade practice responses
- Track preparation progress

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
