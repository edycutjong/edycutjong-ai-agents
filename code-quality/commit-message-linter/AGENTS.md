# AGENTS.md — Commit Message Linter

## Overview
Agent that enforces conventional commit message standards, suggests improvements, and blocks non-conforming commits.

## Tech Stack
- **Stack:** Python

## Features
- Parse commit messages against conventional format
- Validate type prefix (feat, fix, etc.)
- Validate scope format
- Check subject line length
- Check body formatting
- Suggest improvements for vague messages
- Block non-conforming in CI mode
- Support custom type lists
- Angular, Conventional, emoji presets
- JSON report output

## File Structure
- `main.py` — Entry point
- `lib/` — Core logic
- `requirements.txt`
- `README.md`

## Requirements
- No external API keys
- CLI-friendly with JSON output
- CI integration support
