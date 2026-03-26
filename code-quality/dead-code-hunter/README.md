# Dead Code Hunter

Analyze codebase for unused exports, unreachable code paths, orphan files, and dead CSS selectors across JavaScript/TypeScript projects.

## Features
- Detect unused exports in JS/TS
- Find orphan files (not imported anywhere)
- Identify unreachable code paths
- Dead CSS selector detection
- Unused dependency detection
- Report with confidence scores
- Suggested safe deletions
- JSON and Markdown output
- Git-aware (ignore recently added files)

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
