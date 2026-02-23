# AGENTS.md — SOP Generator

## Overview
Reads processes and workflows, generates Standard Operating Procedures with step-by-step instructions. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept process description input
- Generate numbered step-by-step procedures
- Add decision trees for conditional steps
- Include safety/compliance notes
- Generate review and approval workflows
- Add version control metadata
- Include visual aids and diagrams
- Export as formatted Markdown/PDF

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
