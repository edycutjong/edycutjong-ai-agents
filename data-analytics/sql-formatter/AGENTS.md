# AGENTS.md — SQL Formatter

## Overview
SQL Formatter — Format and beautify SQL queries for readability. Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Format SELECT, INSERT, UPDATE, DELETE queries
- Indent nested subqueries
- Uppercase SQL keywords
- Align columns and clauses
- Support multiple SQL dialects


## Files
- main.py
- agent/
- tests/

## Usage
```bash
python main.py <input>
python main.py --help-agent
```

## Design
- CLI-first interaction
- Modular agent definitions
- Import from `agent.formatter` for programmatic use
