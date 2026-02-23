# AGENTS.md — Markdown to PDF Agent

## Overview
Converts styled Markdown documents to beautiful PDFs with headers, footers, and themes. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse Markdown with frontmatter
- Apply customizable PDF themes
- Add headers, footers, page numbers
- Support code syntax highlighting
- Include table of contents
- Handle images and diagrams
- Support custom CSS styling
- Batch convert multiple files

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
