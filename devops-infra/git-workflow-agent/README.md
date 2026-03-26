# Git Workflow Agent

An AI agent that enforces Git workflow best practices, validates commit messages, checks branch naming, and prevents common mistakes.

## Features
- Commit message format validation
- Branch naming convention check
- Pre-push hook validation
- Merge conflict detection
- Large file detection
- Sensitive data scanning
- PR description template enforcement
- Changelog entry verification
- Stale branch identification
- Workflow compliance report

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
