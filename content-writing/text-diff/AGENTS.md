# AGENTS.md — Text Diff Tool

## Overview
Text Diff Tool — Compare two texts and show their differences line by line. Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Line-by-line diff comparison
- Highlight added and removed content
- Unified diff format output
- Side-by-side comparison
- Ignore whitespace option


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
- Import from `agent.differ` for programmatic use
