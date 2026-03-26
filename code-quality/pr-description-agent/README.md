# Pr Description Agent

Auto-generates pull request descriptions from git diffs — includes context, change summary, test coverage, and breaking change warnings.

## Features
- Parse git diff to understand changes
- Generate structured PR description
- Detect breaking changes
- Summarize changes by file/component
- Include test coverage impact
- Add related issue references
- Conventional commit detection
- Screenshot placeholder suggestions
- Reviewer suggestion based on file ownership

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
