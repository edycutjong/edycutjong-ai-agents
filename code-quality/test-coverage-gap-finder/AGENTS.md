# AGENTS.md — Test Coverage Gap Finder

## Overview
Agent that identifies untested code paths by analyzing source and test files, then suggests specific test cases to write.

## Tech Stack
- **Stack:** Python

## Features
- Scan source files for functions/methods
- Scan test files for test cases
- Map tests to source functions
- Identify functions with no tests
- Detect partially tested functions
- Suggest specific test cases
- Priority ranking by code criticality
- Support JS/TS/Python source
- JSON and Markdown report
- CI integration with thresholds

## File Structure
- `main.py` — Entry point
- `lib/` — Core logic
- `requirements.txt`
- `README.md`

## Requirements
- No external API keys
- CLI-friendly with JSON output
- CI integration support
