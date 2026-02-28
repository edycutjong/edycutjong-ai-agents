# AGENTS.md — PR Description Writer

## Overview
Agent that reads a git diff and writes structured PR descriptions with context, change summary, and testing notes.

## Tech Stack
- **Stack:** Python

## Features
- Parse git diff input
- Detect change type and scope
- Generate structured description
- Include file-level change summary
- Suggest testing instructions
- Detect breaking changes
- Link related issues by convention
- Format for GitHub/GitLab templates
- Support multiple description styles
- Configurable templates

## File Structure
- `main.py` — Entry point
- `lib/` — Core logic
- `requirements.txt`
- `README.md`

## Requirements
- No external API keys
- CLI-friendly with JSON output
- CI integration support
