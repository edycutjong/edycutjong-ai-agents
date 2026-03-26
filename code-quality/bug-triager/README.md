# Bug Triager

Issue management agent — Read new GitHub issues.

## Features
- Read new GitHub issues
- Label based on content
- Assign to maintainers
- Check for duplicates
- Reply with template

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
