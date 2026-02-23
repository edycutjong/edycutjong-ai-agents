# AGENTS.md — email-triage-assistant

## Overview
Local AI agent to categorize, summarize, and draft replies to emails.

## Tech Stack
- **Runtime:** Python 3.11+ or Node.js
- **AI:** OpenAI API / Anthropic API / Gemini
- **Framework:** LangChain or custom loop
- **Interface:** CLI or Streamlit

## Features
- Connect IMAP/API\n- Categorize (Urgent, Newsletter, Spam)\n- Summarize threads\n- Draft replies style-matched\n- Local LLM support\n- Privacy focus\n- Daily briefing generation\n- Action item extraction

## File Structure
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings

## Design Notes
Inbox-style UI. Split view.

## Commands
python3 main.py
