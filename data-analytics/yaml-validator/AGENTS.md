# AGENTS.md — YAML Validator

## Overview
YAML Validator — Validate YAML files and report syntax errors. Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Validate YAML syntax
- Report line-level errors
- Check for duplicate keys
- Support multi-document YAML
- Pretty-print parsed output


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
- Import from `agent.validator` for programmatic use
