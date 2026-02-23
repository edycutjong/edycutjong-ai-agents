# AGENTS.md — Blog Post Writer

## Overview
Researches topics, creates outlines, and writes SEO-optimized blog posts with sources. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Research topic with web search
- Generate structured outline
- Write SEO-optimized content
- Add meta description and title tags
- Include relevant source citations
- Optimize keyword density
- Generate social media excerpts
- Export as Markdown/HTML

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
