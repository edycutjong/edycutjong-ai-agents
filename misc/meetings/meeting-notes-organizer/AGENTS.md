# AGENTS.md — meeting-notes-organizer

## Overview
Agent that takes transcripts, extracts tasks, and updates project management tools.

## Tech Stack
- **Runtime:** Python 3.11+ or Node.js
- **AI:** OpenAI API / Anthropic API / Gemini
- **Framework:** LangChain or custom loop
- **Interface:** CLI or Streamlit

## Features
- Transcript ingestion\n- Summary generation\n- Action item extraction\n- API integration (Jira/Linear)\n- Calendar event creation\n- Follow-up email draft\n- Speaker diarization support\n- Searchable archive

## File Structure
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings

## Design Notes
Timeline view. Action card list.

## Commands
python3 main.py
