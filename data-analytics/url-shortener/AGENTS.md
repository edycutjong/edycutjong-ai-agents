# AGENTS.md — URL Shortener

## Overview
URL Shortener — Generate shortened URLs and manage link redirects. Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Generate short unique URLs
- Custom alias support
- Track click analytics
- Validate input URLs
- Bulk URL shortening


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
- Import from `agent.shortener` for programmatic use
