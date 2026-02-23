# AGENTS.md — Paper Summarizer

## Overview
Reads academic papers (arXiv, etc.) and generates plain-language summaries and key takeaways. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse PDF academic papers
- Extract abstract and methodology
- Generate plain-language summary
- Highlight key findings
- Extract citations and references
- Create visual summary
- Support batch processing
- Generate reading lists by topic

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
