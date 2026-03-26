# Test Generation Agent

Agent that analyzes source code and generates unit test suites with edge case coverage.

## Features
- Parse function signatures
- Generate test cases per function
- Edge case identification
- Mock generation for dependencies
- Support for Jest and Vitest
- Multiple assertion styles
- Coverage-driven test generation
- Parameterized test support
- Error path testing
- Test file organization

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
