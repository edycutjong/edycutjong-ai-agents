# Issue Labeler

Agent that auto-labels GitHub issues based on title, body, and file references using keyword matching.

## Features
- GitHub webhook integration
- Keyword-based label matching
- File path reference detection
- Priority assessment (P0-P3)
- Duplicate issue detection
- Auto-assign to team members
- Configurable label rules (YAML)
- Confidence score threshold
- Activity log dashboard
- Dry-run mode

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
