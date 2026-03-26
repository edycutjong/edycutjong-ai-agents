# Test Writer

Agent that analyzes source code and generates unit tests with meaningful assertions and edge cases.

## Features
- Source file analysis
- Test file generation (Jest/Vitest)
- Meaningful assertion generation
- Edge case identification
- Mock/stub suggestions
- Test naming conventions
- Coverage gap detection
- Configurable test framework
- Dry-run preview
- Batch processing

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
