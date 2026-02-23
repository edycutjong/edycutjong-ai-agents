# AGENTS.md — Newsletter Curator

## Overview
Aggregates and summarizes tech news from multiple sources into newsletter-ready format. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Crawl configurable news sources
- Filter by topic relevance
- Generate concise summaries
- Categorize stories by theme
- Rank by importance/trending
- Format as newsletter template
- Include source links
- Support weekly/daily cadence

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
