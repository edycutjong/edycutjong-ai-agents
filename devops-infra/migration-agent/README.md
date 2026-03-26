# Migration Agent

Agent that analyzes a codebase and generates migration plans for framework upgrades.

## Features
- Detect current framework version
- Analyze breaking changes in target version
- Generate step-by-step migration plan
- Identify affected files and functions
- Suggest code transformations
- Risk assessment per change
- Dependency compatibility check
- Migration script generation
- Rollback plan
- Progress tracking

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
