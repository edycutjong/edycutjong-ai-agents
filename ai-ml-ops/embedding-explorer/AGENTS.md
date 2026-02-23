# AGENTS.md — Embedding Explorer

## Overview
Visualizes and searches vector embeddings, finds clusters, outliers, and nearest neighbors. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Load embeddings from files/databases
- Reduce dimensions (t-SNE/UMAP)
- Visualize clusters interactively
- Find nearest neighbors for queries
- Detect outlier embeddings
- Compare embedding models
- Export visualizations
- Support text/image embeddings

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
