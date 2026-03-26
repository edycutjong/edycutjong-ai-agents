# Commit Message Linter

Agent that enforces conventional commit message standards, suggests improvements, and blocks non-conforming commits.

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

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
