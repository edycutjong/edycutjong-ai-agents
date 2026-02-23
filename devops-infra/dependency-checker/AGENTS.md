# AGENTS.md — Dependency Checker

## Overview
Dependency Checker — Check project dependencies for outdated or vulnerable packages. Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Check for outdated packages
- Identify known vulnerabilities
- Support pip, npm, and cargo
- Generate dependency reports
- Suggest version updates


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
- Import from `agent.checker` for programmatic use
