# AGENTS.md — Code Complexity Analyzer

## Overview
Code Complexity Analyzer — Analyze code complexity metrics (cyclomatic complexity, LOC, etc.). Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Calculate cyclomatic complexity
- Count lines of code (LOC)
- Identify complex functions
- Generate complexity reports
- Support multiple languages


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
- Import from `agent.analyzer` for programmatic use
