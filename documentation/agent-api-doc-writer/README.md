# Api Doc Writer

AI agent that generates OpenAPI/Swagger documentation from source code and route definitions

## Features
- Parse route definitions
- Generate OpenAPI 3.0 spec
- Request/response schema inference
- Example value generation
- Markdown documentation output
- Multiple language support
- Update existing docs incrementally
- Validate generated spec

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
