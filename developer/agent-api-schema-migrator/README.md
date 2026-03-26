# Api Schema Migrator

Detects breaking changes between OpenAPI spec versions and generates migration code for API consumers.

## Features
- Compare two OpenAPI/Swagger specs
- Detect breaking vs non-breaking changes
- Generate migration code snippets
- Support REST and GraphQL schemas
- Create changelog from diff
- Type mapping for renamed fields
- Request/response body migration
- Header and auth changes detection
- Export migration guide as markdown
- Configurable ignore rules

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
