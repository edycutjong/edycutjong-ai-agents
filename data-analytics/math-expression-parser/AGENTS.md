# AGENTS.md — Math Expression Parser

## Overview
Math Expression Parser — Parse and evaluate mathematical expressions safely. Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Evaluate arithmetic expressions
- Support parentheses and operator precedence
- Handle trigonometric functions
- Variable substitution
- Step-by-step evaluation


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
- Import from `agent.parser` for programmatic use
