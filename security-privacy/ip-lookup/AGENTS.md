# AGENTS.md — IP Lookup

## Overview
IP Lookup — Look up IP address geolocation and network information. Designed as an AI agent project.

## Tech
- Python 3.10+
- CLI (argparse)
- No external API key required

## Features
- Geolocation lookup (city, country)
- ISP and organization info
- Reverse DNS lookup
- IPv4 and IPv6 support
- Batch IP lookups


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
- Import from `agent.lookup` for programmatic use
