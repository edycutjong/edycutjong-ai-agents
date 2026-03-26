# Pr Description Writer

Agent that reads a git diff and writes structured PR descriptions with context, change summary, and testing notes.

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

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
