# Csv To Api Agent

Takes CSV files and generates REST API servers with CRUD operations automatically.

## Features
- Parse CSV column headers and types
- Generate Express/Flask API server
- Create CRUD endpoints per table
- Add filtering and pagination
- Generate API documentation
- Include data validation
- Support SQLite backend
- Hot-reload on data changes

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
