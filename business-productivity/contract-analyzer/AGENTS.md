# AGENTS.md — Contract Analyzer

## Overview
Reads legal contracts, highlights risky clauses, and suggests amendments. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse PDF/DOCX contracts
- Identify risky clauses
- Flag unusual terms and conditions
- Highlight indemnification clauses
- Check termination terms
- Suggest standard amendments
- Compare against template contracts
- Generate risk assessment report

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
