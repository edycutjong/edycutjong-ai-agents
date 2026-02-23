# AGENTS.md — UUID Generator

## Overview
UUID Generator — Generate and validate UUIDs (v1, v4, v5). Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Generate UUID v1, v4, and v5
- Validate UUID format
- Batch generation support
- Namespace-based UUID v5
- Copy-ready output


## Files
- main.py
- config.py
- requirements.txt
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
- Import from `agent.generator` for programmatic use
