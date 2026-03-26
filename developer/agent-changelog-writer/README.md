# Changelog Writer

Agent that reads git commits, categorizes them, and generates formatted CHANGELOG.md following Keep a Changelog.

## Features
- Parse conventional commits
- Categorize: Added, Changed, Fixed, Removed
- Version number suggestion (semver)
- Breaking change detection
- PR/issue link extraction
- Author attribution
- Multiple output formats (Markdown, JSON)
- Configurable commit parsing rules
- Unreleased section management
- Dry-run preview mode

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
