# Dependency Updater Agent

## Overview
Autonomous agent that scans Python projects for outdated pip dependencies, updates them one by one, runs tests after each update, and rolls back on failure.

## Tech Stack
- **Stack:** Python

## Features
- Scan pip for outdated dependencies
- Prioritize security updates
- Update one dependency at a time
- Run test suite after each update
- Automatic rollback on test failure
- Generate update report
- Support latest/minor/patch strategies
- Ignore list configuration
- Batch mode for monorepos

## Commands
- Run: `python main.py --dir <project_dir>`
- Test: `python -m pytest tests/ -v`

## Design Guidelines
- **Theme:** Dark mode
- **Primary:** `#EC4899`
- **Accent:** `#DB2777`
- **Background:** `#0D1117`

## Requirements
- No external API keys required for core features
- Works standalone and self-contained
- Python 3.9+
