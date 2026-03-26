# Code Reviewer

PR review agent — Fetch PR diff from GitHub.

## Features
- Fetch PR diff from GitHub
- Analyze code quality/bugs
- Post comment suggestions
- Check style guide
- Security scan

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
