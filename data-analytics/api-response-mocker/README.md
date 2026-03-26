# Api Response Mocker

Reads API specs (OpenAPI/Swagger) and generates mock servers with realistic test data.

## Features
- Parse OpenAPI/Swagger specifications
- Generate mock HTTP server
- Return realistic sample responses
- Support dynamic path parameters
- Simulate error responses (4xx/5xx)
- Add configurable latency
- Record and replay requests
- Export as Postman/Insomnia collections

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
