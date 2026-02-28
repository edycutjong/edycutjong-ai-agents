# AGENTS.md — Database Migration Reviewer

## Overview
Agent that reviews SQL migration files for safety — checks for data loss, reversibility, index impact, and lock duration.

## Tech Stack
- **Stack:** Python

## Features
- Parse SQL migration files
- Detect destructive operations (DROP, TRUNCATE)
- Check for reversibility (UP/DOWN)
- Index impact analysis
- Lock duration estimation
- Large table warnings
- Data type change safety check
- Foreign key impact analysis
- Generate safety report
- Block/warn/pass classification

## File Structure
- `main.py` — Entry point
- `lib/` — Core logic
- `requirements.txt`
- `README.md`

## Requirements
- No external API keys
- CLI-friendly with JSON output
- CI integration support
