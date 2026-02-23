# AGENTS.md — Database Diagram Generator

## Overview
Reads database schemas (SQL/ORM) and generates ERD diagrams in Mermaid or PlantUML. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse SQL CREATE TABLE statements
- Read ORM model definitions (SQLAlchemy/Prisma)
- Generate Mermaid ERD diagrams
- Generate PlantUML diagrams
- Show relationships and cardinality
- Color-code tables by module
- Export as SVG/PNG
- Support PostgreSQL/MySQL/SQLite

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
