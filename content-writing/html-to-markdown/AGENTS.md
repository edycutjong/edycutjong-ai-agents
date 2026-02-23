# AGENTS.md — HTML to Markdown Converter

## Overview
HTML to Markdown Converter — Convert HTML content to clean Markdown format. Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Convert HTML tags to Markdown syntax
- Preserve links, images, and formatting
- Handle nested elements and tables
- Clean up whitespace and structure
- Support inline and block elements


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
