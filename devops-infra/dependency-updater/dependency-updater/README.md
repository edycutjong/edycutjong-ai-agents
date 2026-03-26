# Dependency Updater

An AI agent that analyzes project dependencies, checks for updates, evaluates breaking changes, and generates update plans.

## Features
- Scan package.json/requirements.txt
- Check for latest versions
- Identify breaking changes from changelogs
- Generate update priority list
- Risk assessment per update
- Peer dependency conflict detection
- Security advisory integration
- Test compatibility suggestions
- Batch update commands
- Markdown update report

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
