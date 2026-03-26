# Mcp Server Builder

AI agent that scaffolds MCP servers from natural language descriptions — generates tool schemas, handlers, and tests.

## Features
- Parse natural language tool descriptions
- Generate MCP tool schemas (JSON)
- Create handler implementations
- Generate unit tests for each tool
- Support multiple languages (Python, TypeScript)
- Validate schema correctness
- Preview generated server structure
- Export as ready-to-run project
- Support resource and prompt generation
- Configurable templates

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
