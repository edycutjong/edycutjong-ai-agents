# Test Case Generator

Analyzes function signatures and generates comprehensive unit test cases including edge cases and error scenarios.

## Features
- Parse function signatures and types
- Generate happy-path test cases
- Create edge case scenarios
- Generate error handling tests
- Support Python and TypeScript
- Mock external dependencies
- Generate test fixtures
- Boundary value analysis
- Coverage gap detection
- Export as pytest/jest files

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
