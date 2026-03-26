# Documentation Agent

Agent that reads source code and generates comprehensive README and API documentation.

## Features
- Parse source code AST
- Extract function signatures and types
- Generate README.md with overview
- Generate API reference documentation
- Code example extraction
- Dependency documentation
- Environment variable docs
- Installation instructions
- Usage examples from tests
- Markdown and HTML output

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
