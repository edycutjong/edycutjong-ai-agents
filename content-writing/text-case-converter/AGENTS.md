# AGENTS.md — Text Case Converter

## Overview
Text Case Converter — Convert text between different case formats (camelCase, snake_case, etc.). Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Convert to camelCase, PascalCase, snake_case
- Support kebab-case and UPPER_CASE
- Handle title case and sentence case
- Preserve acronyms and numbers
- Batch convert multiple strings


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
- Import from `agent.converter` for programmatic use
