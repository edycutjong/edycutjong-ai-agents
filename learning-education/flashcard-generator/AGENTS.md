# AGENTS.md — Flashcard Generator

## Overview
Reads technical documentation or notes and generates Anki-compatible flashcards. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse Markdown/PDF/TXT input
- Extract key concepts and terms
- Generate question-answer pairs
- Create cloze deletion cards
- Export in Anki-compatible format
- Tag cards by topic/difficulty
- Generate spaced repetition schedule
- Support multiple subjects

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
