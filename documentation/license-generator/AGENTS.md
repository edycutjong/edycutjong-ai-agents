# AGENTS.md — License Generator

## Overview
License Generator — Generate open-source license files (MIT, Apache, GPL, etc.). Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Generate MIT, Apache 2.0, GPL licenses
- Auto-fill author and year
- Support BSD, ISC, and more
- Preview license text
- Output ready-to-use LICENSE file


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
