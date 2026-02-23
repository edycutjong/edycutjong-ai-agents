# AGENTS.md — Invoice Generator Agent

## Overview
Reads project and time tracking data, generates professional PDF invoices. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept client and project details
- Import time tracking data
- Calculate totals with tax
- Generate professional PDF invoices
- Support multiple currencies
- Track payment status
- Generate recurring invoices
- Include payment terms and due dates

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
