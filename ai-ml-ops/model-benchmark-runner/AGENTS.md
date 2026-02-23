# AGENTS.md — Model Benchmark Runner

## Overview
Benchmarks LLM models against test suites, comparing cost, quality, and speed. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Define benchmark test suites
- Run tests across multiple LLM providers
- Measure response time and token usage
- Score output quality automatically
- Calculate cost per query
- Generate comparison tables
- Visualize results with charts
- Support OpenAI/Anthropic/Gemini/local models

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
