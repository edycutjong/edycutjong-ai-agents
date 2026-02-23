# AGENTS.md — HTML to Markdown Converter

## Overview
Scrapes and converts HTML pages to clean, well-formatted Markdown documentation. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse HTML with tag hierarchy
- Convert to clean Markdown
- Preserve headings and lists
- Handle tables and code blocks
- Extract and download images
- Clean up boilerplate/nav/footer
- Support batch URL processing
- Maintain internal link structure

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
