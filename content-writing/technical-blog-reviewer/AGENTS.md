# AGENTS.md — Technical Blog Reviewer

## Overview
Reviews technical articles for accuracy, clarity, code correctness, and completeness. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Check technical accuracy of claims
- Validate code snippets run correctly
- Assess readability and structure
- Flag missing context or prerequisites
- Suggest improved explanations
- Check for outdated information
- Score overall article quality
- Generate editorial feedback report

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
