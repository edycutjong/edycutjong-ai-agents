# Test Generator

Reads source code and generates comprehensive unit and integration test suites with high coverage.

## Features
- Analyze function signatures and types
- Generate unit tests per function
- Generate edge case tests
- Generate integration tests
- Support for Jest and pytest
- Mock dependency generation
- Coverage report integration
- Test description generation

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
