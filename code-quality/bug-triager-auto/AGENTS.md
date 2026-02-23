# AGENTS.md — bug-triager-auto

## Overview
Agent that analyzes incoming bug reports, duplicates, and assigns severity.

## Tech
- **Runtime:** Python 3.11+ or Node.js
- **AI:** OpenAI API / Anthropic API / Gemini
- **Framework:** LangChain or custom loop
- **Interface:** CLI or Streamlit

## Features
- Read issue tracker\n- Detect duplicates/similar issues\n- Assign labels/severity\n- Request missing info\n- Suggest potential fix files\n- Route to correct team\n- Sentiment analysis\n- Close stale issues

## File Structure
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings

## Commands
python3 main.py
