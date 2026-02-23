# AGENTS.md — String Similarity Analyzer

## Overview
String Similarity Analyzer — Compare two strings and calculate their similarity score. Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Calculate similarity percentage
- Support multiple comparison algorithms
- Highlight differences between strings
- Handle Unicode and special characters
- Batch comparison support


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
- Import from `agent.analyzer` for programmatic use
