# AGENTS.md — RAG Evaluator

## Overview
Tests RAG pipeline quality by measuring retrieval accuracy and answer relevance. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Define evaluation test cases
- Measure retrieval precision/recall
- Score answer faithfulness
- Detect hallucinations vs source
- Compare different RAG configurations
- Generate evaluation reports
- Support multiple vector stores
- Benchmark latency and cost

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
