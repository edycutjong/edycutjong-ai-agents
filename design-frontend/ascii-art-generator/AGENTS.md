# AGENTS.md — ASCII Art Generator

## Overview
ASCII Art Generator — Generate ASCII art from text input. Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Convert text to ASCII art banners
- Multiple font styles
- Configurable width and alignment
- Support special characters
- Figlet-compatible output


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
- Import from `agent.generator` for programmatic use
