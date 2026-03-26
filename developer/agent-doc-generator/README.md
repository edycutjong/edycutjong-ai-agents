# Doc Generator

Agent that scans a codebase and generates documentation — README, API docs, and architecture diagrams.

## Features
- Codebase scanning and analysis
- README.md generation with sections
- API endpoint documentation
- Function/class JSDoc extraction
- Architecture diagram generation (Mermaid)
- Usage examples from test files
- Configuration documentation
- Dependency tree visualization
- Output format: Markdown, HTML
- Incremental updates on code changes

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
