# AGENTS.md — sql-query-builder-agent

## Overview
Natural language to SQL agent. Connects to schema, writes safe queries.

## Tech Stack
- **Runtime:** Python 3.11+ or Node.js
- **AI:** OpenAI API / Anthropic API / Gemini
- **Framework:** LangChain or custom loop
- **Interface:** CLI or Streamlit

## Features
- Schema introspection\n- Question answering\n- Query generation\n- Explain query plan\n- Optimization suggestions\n- Read-only mode enforcement\n- Multi-dialect support\n- Visual result preview

## File Structure
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings

## Design Notes
Chat interface for data.

## Commands
python3 main.py
