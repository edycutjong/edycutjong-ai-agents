# AGENTS.md — Cron Parser

## Overview
Cron Parser — Parse and explain cron expressions in human-readable format. Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Parse standard cron expressions
- Human-readable explanation
- Show next N run times
- Validate cron syntax
- Support extended cron format


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
- Import from `agent.parser` for programmatic use
