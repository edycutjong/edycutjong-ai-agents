# AGENTS.md — Expense Categorizer

## Overview
Reads bank statements and receipts, auto-categorizes expenses for bookkeeping. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse bank statement CSVs
- OCR receipt images
- Auto-categorize transactions
- Detect recurring subscriptions
- Flag unusual spending
- Generate monthly expense reports
- Support multiple currencies
- Export for tax preparation

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
