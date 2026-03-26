# Readme Keeper

Agent that monitors code changes and keeps README.md in sync — updates install steps, API docs, and examples.

## Features
- Monitor file changes via git hooks
- Detect outdated README sections
- Auto-update installation steps
- Sync API documentation with code
- Update example code snippets
- Badge freshness check
- PR creation for README updates
- Section scan for accuracy
- Support multiple README formats
- Configurable section watching

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
