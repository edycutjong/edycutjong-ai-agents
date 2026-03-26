# AI Code Review Agent

Autonomous code review agent that finds bugs, style issues, and suggests improvements

## Features
- Parse source code files
- Detect common bug patterns
- Style consistency checking
- Code complexity scoring
- Unused variable detection
- Security vulnerability flagging
- Improvement suggestions with diffs
- Support for JS, TS, Python
- JSON report output
- Configurable rule sets

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
