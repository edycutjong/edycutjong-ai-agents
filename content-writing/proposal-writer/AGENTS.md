# AGENTS.md — Proposal Writer

## Overview
Generates project proposals from requirements with timeline, budget estimates, and deliverables. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept project requirements input
- Generate executive summary
- Create detailed scope of work
- Estimate timeline with milestones
- Calculate budget breakdown
- List deliverables and acceptance criteria
- Include risk assessment section
- Export as PDF/Markdown

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
