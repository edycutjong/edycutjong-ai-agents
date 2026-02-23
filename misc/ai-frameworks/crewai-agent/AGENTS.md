# AGENTS.md — CrewAI Agent

## Overview
A multi-agent crew that collaborates to research topics, write reports, and generate insights. Uses CrewAI for agent orchestration.

## Tech
- Python 3.12, CrewAI, OpenAI API
- Rich for terminal output

## Features
- 3-agent crew: Researcher, Writer, Editor
- Researcher: searches web, gathers data, extracts key facts
- Writer: synthesizes research into structured report
- Editor: reviews, improves clarity, checks accuracy
- Sequential task execution with handoffs
- Output as formatted markdown report
- Configurable topics via CLI args
- Verbose mode showing agent reasoning

## Files
- `crew.py` — Crew definition with agents and tasks
- `agents/researcher.py` — Research agent with search tools
- `agents/writer.py` — Writing agent with formatting
- `agents/editor.py` — Editing agent with quality checks
- `tools/` — Custom tools (web_search, summarize)
- `cli.py` — CLI entry point
- `requirements.txt`
- `.env.example` — OPENAI_API_KEY

## Commands
```bash
pip install -r requirements.txt
python cli.py --topic "AI trends 2025"
python cli.py --topic "market analysis" --verbose
pytest
```
