# AGENTS.md — Responsive Design Tester

## Overview
Screenshots web pages at multiple viewports and flags layout issues automatically. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Capture screenshots at multiple breakpoints
- Detect layout overflow issues
- Flag text truncation problems
- Check touch target sizes on mobile
- Compare against design mockups
- Generate responsive audit report
- Support custom viewport sizes
- Test horizontal scrolling issues

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
