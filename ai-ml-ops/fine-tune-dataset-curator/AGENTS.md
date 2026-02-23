# AGENTS.md — Fine-Tune Dataset Curator

## Overview
Curates and formats datasets for LLM fine-tuning in JSONL and chat formats. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept raw text/conversation data
- Clean and deduplicate entries
- Format for OpenAI fine-tuning (JSONL)
- Format for Hugging Face datasets
- Validate data quality and consistency
- Balance dataset categories
- Split train/validation sets
- Generate dataset statistics

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
