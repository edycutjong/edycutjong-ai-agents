# AGENTS.md — Color Converter

## Overview
Color Converter — Convert between color formats (HEX, RGB, HSL). Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Convert HEX to RGB and HSL
- Convert RGB to HEX and HSL
- Convert HSL to HEX and RGB
- Color name lookup
- Batch color conversion


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
