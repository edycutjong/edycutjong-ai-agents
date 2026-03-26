# Code Smell Detector

AI agent that scans codebases for common code smells and suggests refactoring patterns

## Features
- Detect common code smells
- Long method detection
- God class identification
- Feature envy analysis
- Refactoring suggestions
- Severity scoring
- File-by-file report
- CI integration support

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
