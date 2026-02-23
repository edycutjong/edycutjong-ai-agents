# AGENTS.md — research-summarizer-agent

## Overview
Deep research agent. Give a topic, it browses, reads, and synthesizes a report.

## Tech Stack
- **Runtime:** Python 3.11+ or Node.js
- **AI:** OpenAI API / Anthropic API / Gemini
- **Framework:** LangChain or custom loop
- **Interface:** CLI or Streamlit

## Features
- Multi-step web browsing\n- Source citation\n- Synthesize multiple sources\n- Generate PDF/Markdown report\n- Fact checking step\n- Configurable depth\n- Specific domain filtering\n- Save research history

## File Structure
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings

## Design Notes
Research dashboard. Knowledge graph.

## Commands
python3 main.py
