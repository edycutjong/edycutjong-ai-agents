# AGENTS.md — documentation-writer-bot

## Overview
Agent that reads codebases and generates/updates documentation folders.

## Tech Stack
- **Runtime:** Python 3.11+ or Node.js
- **AI:** OpenAI API / Anthropic API / Gemini
- **Framework:** LangChain or custom loop
- **Interface:** CLI or Streamlit

## Features
- Scan file structure\n- Read code (functions/classes)\n- Generate Markdown docs\n- Update existing docs (diff aware)\n- Create diagrams (Mermaid)\n- API reference generation\n- Commit changes\n- Tone configuration

## File Structure
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings

## Design Notes
Interactive CLI. Progress bars.

## Commands
python3 main.py
