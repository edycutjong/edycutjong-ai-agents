# Database Diagram Generator

## Overview
Reads database schemas (SQL/ORM) and generates ERD diagrams in Mermaid or PlantUML.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

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
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module

## API Keys
- `GEMINI_API_KEY` — Required

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
